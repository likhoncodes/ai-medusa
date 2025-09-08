"""
Multi-Agent Parallel Execution System
=====================================

This script demonstrates advanced multi-agent browser automation with:
- Parallel task execution across multiple browser instances
- Agent coordination and communication
- Load balancing and resource management
- Fault tolerance and error recovery
- Real-time monitoring and reporting
"""

import asyncio
import json
import time
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from concurrent.futures import ThreadPoolExecutor
import uuid

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AgentStatus(Enum):
    """Agent status enumeration"""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"

class TaskPriority(Enum):
    """Task priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class Task:
    """Task data structure"""
    id: str
    name: str
    description: str
    url: str
    actions: List[str]
    priority: TaskPriority
    timeout: int
    retry_count: int
    created_at: Optional[float] = None
    assigned_agent: Optional[str] = None
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@dataclass
class Agent:
    """Agent data structure"""
    id: str
    name: str
    status: AgentStatus
    current_task: Optional[str]
    completed_tasks: int
    failed_tasks: int
    total_execution_time: float
    last_activity: float
    capabilities: List[str]
    max_concurrent_tasks: int = 1

class MockBrowserAgent:
    """Mock browser agent for demonstration"""
    
    def __init__(self, agent_id: str, capabilities: List[str]):
        self.id = agent_id
        self.capabilities = capabilities
        self.is_busy = False
    
    async def execute_task(self, task: Task) -> Dict[str, Any]:
        """Execute a browser automation task"""
        try:
            logger.info(f"Agent {self.id} executing task: {task.name}")
            self.is_busy = True
            
            # Simulate task execution time
            execution_time = min(task.timeout, 5)  # Max 5 seconds for demo
            await asyncio.sleep(execution_time)
            
            # Simulate success/failure based on task complexity
            success_rate = 0.9 if task.priority != TaskPriority.CRITICAL else 0.95
            success = time.time() % 1 < success_rate
            
            if success:
                result = {
                    "success": True,
                    "execution_time": execution_time,
                    "actions_completed": len(task.actions),
                    "data": f"Mock result for task {task.name}",
                    "screenshots": [f"screenshot_{task.id}_{i}.png" for i in range(2)]
                }
            else:
                result = {
                    "success": False,
                    "error": f"Mock error in task {task.name}",
                    "execution_time": execution_time
                }
            
            self.is_busy = False
            return result
            
        except Exception as e:
            self.is_busy = False
            return {"success": False, "error": str(e)}

class AgentManager:
    """
    Manages multiple browser automation agents
    """
    
    def __init__(self, max_agents: int = 5):
        self.max_agents = max_agents
        self.agents: Dict[str, Agent] = {}
        self.browser_agents: Dict[str, MockBrowserAgent] = {}
        self.task_queue: List[Task] = []
        self.completed_tasks: List[Task] = []
        self.active_tasks: Dict[str, Task] = {}
        self.is_running = False
        self.stats = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "average_execution_time": 0,
            "start_time": 0
        }
    
    async def initialize(self):
        """Initialize the agent manager and create agents"""
        try:
            logger.info(f"Initializing {self.max_agents} agents...")
            
            # Create agents with different capabilities
            agent_configs = [
                {"name": "WebScraper", "capabilities": ["scraping", "data_extraction", "screenshots"]},
                {"name": "FormFiller", "capabilities": ["form_filling", "authentication", "validation"]},
                {"name": "Tester", "capabilities": ["testing", "validation", "performance_monitoring"]},
                {"name": "Monitor", "capabilities": ["monitoring", "health_checks", "reporting"]},
                {"name": "GeneralPurpose", "capabilities": ["general", "backup", "flexible"]}
            ]
            
            for i in range(min(self.max_agents, len(agent_configs))):
                config = agent_configs[i]
                agent_id = f"agent_{i+1}"
                
                # Create agent data structure
                agent = Agent(
                    id=agent_id,
                    name=config["name"],
                    status=AgentStatus.IDLE,
                    current_task=None,
                    completed_tasks=0,
                    failed_tasks=0,
                    total_execution_time=0,
                    last_activity=time.time(),
                    capabilities=config["capabilities"]
                )
                
                # Create browser agent
                browser_agent = MockBrowserAgent(agent_id, config["capabilities"])
                
                self.agents[agent_id] = agent
                self.browser_agents[agent_id] = browser_agent
            
            self.stats["start_time"] = time.time()
            logger.info(f"Agent manager initialized with {len(self.agents)} agents")
            
        except Exception as e:
            logger.error(f"Error initializing agent manager: {str(e)}")
    
    def add_task(self, task: Task):
        """Add a task to the queue"""
        task.created_at = time.time()
        self.task_queue.append(task)
        self.stats["total_tasks"] += 1
        
        # Sort queue by priority
        self.task_queue.sort(key=lambda t: t.priority.value, reverse=True)
        
        logger.info(f"Task added to queue: {task.name} (Priority: {task.priority.name})")
    
    def add_tasks_batch(self, tasks: List[Task]):
        """Add multiple tasks to the queue"""
        for task in tasks:
            self.add_task(task)
        
        logger.info(f"Added {len(tasks)} tasks to queue")
    
    async def start_execution(self):
        """Start the multi-agent execution system"""
        if self.is_running:
            logger.warning("Agent manager is already running")
            return
        
        self.is_running = True
        logger.info("Starting multi-agent execution system...")
        
        # Start task distribution and monitoring
        await asyncio.gather(
            self._task_distributor(),
            self._agent_monitor(),
            self._performance_tracker()
        )
    
    async def stop_execution(self):
        """Stop the execution system"""
        self.is_running = False
        logger.info("Stopping multi-agent execution system...")
    
    async def _task_distributor(self):
        """Distribute tasks to available agents"""
        while self.is_running:
            try:
                if not self.task_queue:
                    await asyncio.sleep(1)
                    continue
                
                # Find available agents
                available_agents = [
                    agent_id for agent_id, agent in self.agents.items()
                    if agent.status == AgentStatus.IDLE
                ]
                
                if not available_agents:
                    await asyncio.sleep(0.5)
                    continue
                
                # Assign tasks to agents
                tasks_to_assign = min(len(self.task_queue), len(available_agents))
                
                for i in range(tasks_to_assign):
                    task = self.task_queue.pop(0)
                    agent_id = self._select_best_agent(task, available_agents)
                    
                    if agent_id:
                        await self._assign_task_to_agent(task, agent_id)
                        available_agents.remove(agent_id)
                
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error in task distributor: {str(e)}")
                await asyncio.sleep(1)
    
    def _select_best_agent(self, task: Task, available_agents: List[str]) -> Optional[str]:
        """Select the best agent for a task based on capabilities and load"""
        best_agent = None
        best_score = -1
        
        for agent_id in available_agents:
            agent = self.agents[agent_id]
            score = 0
            
            # Capability matching
            task_requirements = self._extract_task_requirements(task)
            matching_capabilities = len(set(agent.capabilities) & set(task_requirements))
            score += matching_capabilities * 10
            
            # Load balancing (prefer agents with fewer completed tasks)
            if agent.completed_tasks == 0:
                score += 5  # Bonus for unused agents
            else:
                score -= agent.completed_tasks * 0.1
            
            # Success rate consideration
            if agent.completed_tasks > 0:
                success_rate = agent.completed_tasks / (agent.completed_tasks + agent.failed_tasks)
                score += success_rate * 5
            
            if score > best_score:
                best_score = score
                best_agent = agent_id
        
        return best_agent
    
    def _extract_task_requirements(self, task: Task) -> List[str]:
        """Extract required capabilities from task description"""
        requirements = []
        
        # Simple keyword matching for demo
        if "form" in task.description.lower():
            requirements.append("form_filling")
        if "scrape" in task.description.lower() or "extract" in task.description.lower():
            requirements.append("scraping")
        if "test" in task.description.lower():
            requirements.append("testing")
        if "monitor" in task.description.lower():
            requirements.append("monitoring")
        
        return requirements if requirements else ["general"]
    
    async def _assign_task_to_agent(self, task: Task, agent_id: str):
        """Assign a task to a specific agent"""
        try:
            agent = self.agents[agent_id]
            browser_agent = self.browser_agents[agent_id]
            
            # Update agent status
            agent.status = AgentStatus.BUSY
            agent.current_task = task.id
            agent.last_activity = time.time()
            
            # Update task
            task.assigned_agent = agent_id
            task.started_at = time.time()
            self.active_tasks[task.id] = task
            
            logger.info(f"Task {task.name} assigned to agent {agent_id}")
            
            # Execute task asynchronously
            asyncio.create_task(self._execute_task(task, agent, browser_agent))
            
        except Exception as e:
            logger.error(f"Error assigning task: {str(e)}")
    
    async def _execute_task(self, task: Task, agent: Agent, browser_agent: MockBrowserAgent):
        """Execute a task with an agent"""
        try:
            start_time = time.time()
            
            # Execute the task
            result = await browser_agent.execute_task(task)
            
            execution_time = time.time() - start_time
            
            # Update task result
            task.completed_at = time.time()
            task.result = result
            
            if result.get("success", False):
                agent.completed_tasks += 1
                self.stats["completed_tasks"] += 1
                logger.info(f"Task {task.name} completed successfully by agent {agent.id}")
            else:
                task.error = result.get("error", "Unknown error")
                agent.failed_tasks += 1
                self.stats["failed_tasks"] += 1
                logger.error(f"Task {task.name} failed on agent {agent.id}: {task.error}")
            
            # Update agent status
            agent.status = AgentStatus.IDLE
            agent.current_task = None
            agent.total_execution_time += execution_time
            agent.last_activity = time.time()
            
            # Move task to completed
            if task.id in self.active_tasks:
                del self.active_tasks[task.id]
            self.completed_tasks.append(task)
            
        except Exception as e:
            logger.error(f"Error executing task {task.name}: {str(e)}")
            
            # Handle error
            task.error = str(e)
            task.completed_at = time.time()
            agent.status = AgentStatus.ERROR
            agent.failed_tasks += 1
            self.stats["failed_tasks"] += 1
            
            # Move to completed with error
            if task.id in self.active_tasks:
                del self.active_tasks[task.id]
            self.completed_tasks.append(task)
    
    async def _agent_monitor(self):
        """Monitor agent health and performance"""
        while self.is_running:
            try:
                current_time = time.time()
                
                for agent_id, agent in self.agents.items():
                    # Check for stuck agents
                    if agent.status == AgentStatus.BUSY:
                        if current_time - agent.last_activity > 30:  # 30 seconds timeout
                            logger.warning(f"Agent {agent_id} appears stuck, resetting...")
                            agent.status = AgentStatus.IDLE
                            agent.current_task = None
                    
                    # Check for error recovery
                    elif agent.status == AgentStatus.ERROR:
                        if current_time - agent.last_activity > 10:  # 10 seconds recovery time
                            logger.info(f"Recovering agent {agent_id} from error state")
                            agent.status = AgentStatus.IDLE
                
                await asyncio.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                logger.error(f"Error in agent monitor: {str(e)}")
                await asyncio.sleep(5)
    
    async def _performance_tracker(self):
        """Track and log performance metrics"""
        while self.is_running:
            try:
                # Calculate average execution time
                if self.stats["completed_tasks"] > 0:
                    total_time = sum(agent.total_execution_time for agent in self.agents.values())
                    self.stats["average_execution_time"] = total_time / self.stats["completed_tasks"]
                
                # Log performance summary every 30 seconds
                await asyncio.sleep(30)
                
                if self.stats["total_tasks"] > 0:
                    logger.info(f"Performance Summary - Total: {self.stats['total_tasks']}, "
                              f"Completed: {self.stats['completed_tasks']}, "
                              f"Failed: {self.stats['failed_tasks']}, "
                              f"Success Rate: {(self.stats['completed_tasks']/self.stats['total_tasks'])*100:.1f}%")
                
            except Exception as e:
                logger.error(f"Error in performance tracker: {str(e)}")
                await asyncio.sleep(30)
    
    def get_status_report(self) -> Dict[str, Any]:
        """Get comprehensive status report"""
        current_time = time.time()
        
        # Agent status summary
        agent_summary = {}
        for agent_id, agent in self.agents.items():
            agent_summary[agent_id] = {
                "name": agent.name,
                "status": agent.status.value,
                "completed_tasks": agent.completed_tasks,
                "failed_tasks": agent.failed_tasks,
                "success_rate": (agent.completed_tasks / max(agent.completed_tasks + agent.failed_tasks, 1)) * 100,
                "average_execution_time": agent.total_execution_time / max(agent.completed_tasks, 1),
                "capabilities": agent.capabilities
            }
        
        # Queue status
        queue_summary = {
            "pending_tasks": len(self.task_queue),
            "active_tasks": len(self.active_tasks),
            "completed_tasks": len(self.completed_tasks),
            "tasks_by_priority": {
                priority.name: len([t for t in self.task_queue if t.priority == priority])
                for priority in TaskPriority
            }
        }
        
        # Overall statistics
        runtime = current_time - self.stats["start_time"]
        overall_stats = {
            **self.stats,
            "runtime_seconds": runtime,
            "tasks_per_minute": (self.stats["completed_tasks"] / max(runtime / 60, 1)),
            "active_agents": len([a for a in self.agents.values() if a.status == AgentStatus.BUSY]),
            "idle_agents": len([a for a in self.agents.values() if a.status == AgentStatus.IDLE])
        }
        
        return {
            "agents": agent_summary,
            "queue": queue_summary,
            "statistics": overall_stats,
            "timestamp": current_time
        }

# Example usage and demonstrations
async def demo_multi_agent_system():
    """Demonstrate multi-agent parallel execution"""
    
    # Initialize agent manager
    manager = AgentManager(max_agents=3)
    await manager.initialize()
    
    # Create sample tasks
    sample_tasks = [
        Task(
            id=str(uuid.uuid4()),
            name="Scrape Product Data",
            description="Extract product information from e-commerce site",
            url="https://example-shop.com/products",
            actions=["navigate", "extract_data", "screenshot"],
            priority=TaskPriority.HIGH,
            timeout=30,
            retry_count=2
        ),
        Task(
            id=str(uuid.uuid4()),
            name="Fill Registration Form",
            description="Complete user registration form with test data",
            url="https://example.com/register",
            actions=["fill_form", "submit", "verify"],
            priority=TaskPriority.NORMAL,
            timeout=20,
            retry_count=1
        ),
        Task(
            id=str(uuid.uuid4()),
            name="Performance Test",
            description="Run performance tests on landing page",
            url="https://example.com/landing",
            actions=["load_test", "measure_metrics", "report"],
            priority=TaskPriority.CRITICAL,
            timeout=60,
            retry_count=3
        ),
        Task(
            id=str(uuid.uuid4()),
            name="Monitor Health Check",
            description="Check system health and availability",
            url="https://example.com/health",
            actions=["ping", "check_status", "log_results"],
            priority=TaskPriority.LOW,
            timeout=10,
            retry_count=1
        ),
        Task(
            id=str(uuid.uuid4()),
            name="Data Validation",
            description="Validate form data and business rules",
            url="https://example.com/validate",
            actions=["test_validation", "check_errors", "report"],
            priority=TaskPriority.HIGH,
            timeout=25,
            retry_count=2
        )
    ]
    
    try:
        # Add tasks to queue
        manager.add_tasks_batch(sample_tasks)
        
        # Start execution system
        execution_task = asyncio.create_task(manager.start_execution())
        
        # Monitor progress
        for i in range(12):  # Monitor for 60 seconds (12 * 5 seconds)
            await asyncio.sleep(5)
            
            status_report = manager.get_status_report()
            
            print(f"\n--- Status Report (T+{i*5}s) ---")
            print(f"Queue: {status_report['queue']['pending_tasks']} pending, "
                  f"{status_report['queue']['active_tasks']} active, "
                  f"{status_report['queue']['completed_tasks']} completed")
            print(f"Agents: {status_report['statistics']['active_agents']} busy, "
                  f"{status_report['statistics']['idle_agents']} idle")
            print(f"Success Rate: {(status_report['statistics']['completed_tasks']/max(status_report['statistics']['total_tasks'], 1))*100:.1f}%")
            
            # Stop if all tasks completed
            if (status_report['queue']['pending_tasks'] == 0 and 
                status_report['queue']['active_tasks'] == 0 and
                status_report['queue']['completed_tasks'] > 0):
                break
        
        # Stop execution
        await manager.stop_execution()
        
        # Final report
        final_report = manager.get_status_report()
        
        print("\n" + "="*50)
        print("FINAL EXECUTION REPORT")
        print("="*50)
        
        with open("multi_agent_report.json", "w") as f:
            json.dump(final_report, f, indent=2)
        
        print(f"Total Tasks: {final_report['statistics']['total_tasks']}")
        print(f"Completed: {final_report['statistics']['completed_tasks']}")
        print(f"Failed: {final_report['statistics']['failed_tasks']}")
        print(f"Success Rate: {(final_report['statistics']['completed_tasks']/max(final_report['statistics']['total_tasks'], 1))*100:.1f}%")
        print(f"Average Execution Time: {final_report['statistics']['average_execution_time']:.2f}s")
        print(f"Tasks per Minute: {final_report['statistics']['tasks_per_minute']:.1f}")
        
        print("\nAgent Performance:")
        for agent_id, agent_data in final_report['agents'].items():
            print(f"  {agent_data['name']}: {agent_data['completed_tasks']} completed, "
                  f"{agent_data['success_rate']:.1f}% success rate")
        
        print("\nMulti-agent execution demo completed!")
        
    except Exception as e:
        logger.error(f"Demo error: {str(e)}")
        await manager.stop_execution()

if __name__ == "__main__":
    print("Multi-Agent Parallel Execution Demo")
    print("=" * 40)
    
    # Run demonstration
    asyncio.run(demo_multi_agent_system())
