# Browser Automation Instructions

## Playwright Integration Patterns

### Custom Action Implementation
\`\`\`python
from playwright.async_api import Page, Locator
from typing import Dict, Any, Optional

class PlaywrightActions:
    def __init__(self, page: Page):
        self.page = page
    
    async def smart_fill_form(self, form_data: Dict[str, Any]) -> Dict[str, str]:
        """Fill form fields intelligently based on field types and labels"""
        results = {}
        
        for field_name, value in form_data.items():
            try:
                # Try multiple selector strategies
                selectors = [
                    f'input[name="{field_name}"]',
                    f'input[id="{field_name}"]',
                    f'textarea[name="{field_name}"]',
                    f'select[name="{field_name}"]'
                ]
                
                element = None
                for selector in selectors:
                    try:
                        element = await self.page.wait_for_selector(selector, timeout=2000)
                        break
                    except:
                        continue
                
                if element:
                    await element.fill(str(value))
                    results[field_name] = "success"
                else:
                    results[field_name] = "field_not_found"
                    
            except Exception as e:
                results[field_name] = f"error: {str(e)}"
        
        return results
\`\`\`

### Screenshot and Text Extraction
\`\`\`python
async def capture_element_screenshot(
    self, 
    selector: str, 
    filename: Optional[str] = None
) -> bytes:
    """Capture screenshot of specific element"""
    element = await self.page.wait_for_selector(selector)
    screenshot = await element.screenshot()
    
    if filename:
        with open(filename, 'wb') as f:
            f.write(screenshot)
    
    return screenshot

async def extract_structured_text(self, selectors: Dict[str, str]) -> Dict[str, str]:
    """Extract text from multiple elements with structured output"""
    results = {}
    
    for key, selector in selectors.items():
        try:
            element = await self.page.wait_for_selector(selector, timeout=5000)
            text = await element.inner_text()
            results[key] = text.strip()
        except:
            results[key] = None
    
    return results
\`\`\`

## Browser-Use with OpenAI Integration

### AI-Guided Automation
\`\`\`python
from browser_use import Agent
from openai import AsyncOpenAI

class AIBrowserAgent:
    def __init__(self, openai_api_key: str):
        self.client = AsyncOpenAI(api_key=openai_api_key)
        self.agent = Agent(
            task="Navigate and interact with web pages intelligently",
            llm=self.client,
            use_vision=True
        )
    
    async def perform_task(self, instruction: str, url: str) -> Dict[str, Any]:
        """Execute complex web tasks using AI guidance"""
        try:
            result = await self.agent.run(
                f"Go to {url} and {instruction}",
                max_steps=10
            )
            
            return {
                "success": True,
                "result": result,
                "steps_taken": len(result.history),
                "final_url": result.final_url
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "steps_taken": 0
            }
\`\`\`

### Multi-Step Workflow Automation
\`\`\`python
async def execute_workflow(self, workflow_steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Execute a series of automated steps with AI decision making"""
    results = []
    
    for step in workflow_steps:
        step_type = step.get("type")
        
        if step_type == "navigate":
            await self.agent.page.goto(step["url"])
            
        elif step_type == "ai_action":
            result = await self.perform_task(step["instruction"], step.get("context", ""))
            results.append(result)
            
        elif step_type == "extract_data":
            data = await self.extract_structured_text(step["selectors"])
            results.append({"type": "extraction", "data": data})
            
        elif step_type == "screenshot":
            screenshot = await self.capture_element_screenshot(step["selector"])
            results.append({"type": "screenshot", "size": len(screenshot)})
    
    return results
\`\`\`

## Chrome DevTools Protocol (CDP) Integration

### Performance Monitoring
\`\`\`python
import asyncio
from playwright.async_api import CDPSession

class CDPMonitor:
    def __init__(self, page: Page):
        self.page = page
        self.cdp_session: CDPSession = None
        self.performance_metrics = []
        self.network_events = []
    
    async def start_monitoring(self):
        """Initialize CDP session and enable monitoring"""
        self.cdp_session = await self.page.context.new_cdp_session(self.page)
        
        # Enable performance monitoring
        await self.cdp_session.send("Performance.enable")
        await self.cdp_session.send("Network.enable")
        
        # Set up event listeners
        self.cdp_session.on("Performance.metrics", self._handle_performance_metrics)
        self.cdp_session.on("Network.responseReceived", self._handle_network_response)
    
    async def _handle_performance_metrics(self, event):
        """Handle performance metrics events"""
        metrics = event.get("metrics", [])
        timestamp = event.get("timestamp")
        
        self.performance_metrics.append({
            "timestamp": timestamp,
            "metrics": {metric["name"]: metric["value"] for metric in metrics}
        })
    
    async def _handle_network_response(self, event):
        """Handle network response events"""
        response = event.get("response", {})
        self.network_events.append({
            "url": response.get("url"),
            "status": response.get("status"),
            "mimeType": response.get("mimeType"),
            "timestamp": event.get("timestamp")
        })
    
    async def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        # Get runtime metrics
        runtime_metrics = await self.cdp_session.send("Performance.getMetrics")
        
        return {
            "runtime_metrics": runtime_metrics,
            "performance_timeline": self.performance_metrics,
            "network_summary": {
                "total_requests": len(self.network_events),
                "failed_requests": len([e for e in self.network_events if e["status"] >= 400]),
                "resource_types": {}
            }
        }
\`\`\`

## Multi-Agent Parallel Execution

### Parallel Task Execution
\`\`\`python
import asyncio
from typing import List, Callable, Any
from concurrent.futures import ThreadPoolExecutor

class MultiAgentExecutor:
    def __init__(self, max_concurrent_agents: int = 5):
        self.max_concurrent = max_concurrent_agents
        self.semaphore = asyncio.Semaphore(max_concurrent_agents)
    
    async def execute_parallel_tasks(
        self, 
        tasks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Execute multiple browser automation tasks in parallel"""
        
        async def execute_single_task(task: Dict[str, Any]) -> Dict[str, Any]:
            async with self.semaphore:
                agent = AIBrowserAgent(task["openai_api_key"])
                
                try:
                    result = await agent.perform_task(
                        task["instruction"], 
                        task["url"]
                    )
                    return {
                        "task_id": task["id"],
                        "success": True,
                        "result": result,
                        "execution_time": result.get("execution_time", 0)
                    }
                except Exception as e:
                    return {
                        "task_id": task["id"],
                        "success": False,
                        "error": str(e),
                        "execution_time": 0
                    }
        
        # Execute all tasks concurrently
        results = await asyncio.gather(
            *[execute_single_task(task) for task in tasks],
            return_exceptions=True
        )
        
        return results
    
    async def execute_with_load_balancing(
        self, 
        tasks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Execute tasks with intelligent load balancing"""
        
        # Sort tasks by estimated complexity
        sorted_tasks = sorted(tasks, key=lambda x: x.get("complexity", 1), reverse=True)
        
        # Execute in batches
        batch_size = self.max_concurrent
        results = []
        
        for i in range(0, len(sorted_tasks), batch_size):
            batch = sorted_tasks[i:i + batch_size]
            batch_results = await self.execute_parallel_tasks(batch)
            results.extend(batch_results)
        
        return {
            "total_tasks": len(tasks),
            "successful_tasks": len([r for r in results if r.get("success", False)]),
            "failed_tasks": len([r for r in results if not r.get("success", False)]),
            "results": results
        }
\`\`\`

### Error Handling and Retry Logic
\`\`\`python
async def execute_with_retry(
    self, 
    task: Dict[str, Any], 
    max_retries: int = 3
) -> Dict[str, Any]:
    """Execute task with retry logic and exponential backoff"""
    
    for attempt in range(max_retries + 1):
        try:
            result = await self.execute_single_task(task)
            if result["success"]:
                return result
        except Exception as e:
            if attempt == max_retries:
                return {
                    "task_id": task["id"],
                    "success": False,
                    "error": f"Failed after {max_retries} retries: {str(e)}",
                    "attempts": attempt + 1
                }
            
            # Exponential backoff
            wait_time = 2 ** attempt
            await asyncio.sleep(wait_time)
    
    return {"success": False, "error": "Max retries exceeded"}
