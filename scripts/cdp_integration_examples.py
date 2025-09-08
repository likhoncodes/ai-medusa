"""
Chrome DevTools Protocol (CDP) Integration Examples
===================================================

This script demonstrates advanced CDP integration for:
- Performance monitoring and optimization
- Network traffic analysis
- JavaScript debugging and profiling
- Memory usage tracking
- Custom browser behavior modification
"""

import asyncio
import json
import time
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
import logging
from pathlib import Path

# Note: In real implementation, you would use:
# from playwright.async_api import async_playwright, CDPSession
# For this demo, we'll create mock classes

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Performance metrics data structure"""
    navigation_start: float
    dom_content_loaded: float
    load_complete: float
    first_paint: float
    first_contentful_paint: float
    largest_contentful_paint: float
    cumulative_layout_shift: float
    first_input_delay: float
    total_blocking_time: float

@dataclass
class NetworkRequest:
    """Network request data structure"""
    request_id: str
    url: str
    method: str
    status_code: int
    response_time: float
    response_size: int
    request_headers: Dict[str, str]
    response_headers: Dict[str, str]
    timestamp: float

@dataclass
class MemoryUsage:
    """Memory usage data structure"""
    used_js_heap_size: int
    total_js_heap_size: int
    js_heap_size_limit: int
    timestamp: float

class MockCDPSession:
    """Mock CDP session for demonstration"""
    
    def __init__(self):
        self.event_handlers: Dict[str, List[Callable]] = {}
        self.enabled_domains: List[str] = []
    
    async def send(self, method: str, params: Dict = None) -> Dict[str, Any]:
        """Mock CDP command sending"""
        logger.info(f"CDP Command: {method}")
        
        # Mock responses for different commands
        if method == "Performance.getMetrics":
            return {
                "metrics": [
                    {"name": "NavigationStart", "value": time.time() * 1000},
                    {"name": "DOMContentLoaded", "value": time.time() * 1000 + 500},
                    {"name": "LoadEventEnd", "value": time.time() * 1000 + 1000}
                ]
            }
        elif method == "Runtime.evaluate":
            return {"result": {"value": "Mock evaluation result"}}
        elif method == "Memory.getDOMCounters":
            return {
                "documents": 5,
                "nodes": 1250,
                "jsEventListeners": 45
            }
        
        return {"success": True}
    
    def on(self, event: str, handler: Callable):
        """Register event handler"""
        if event not in self.event_handlers:
            self.event_handlers[event] = []
        self.event_handlers[event].append(handler)
    
    async def emit_mock_event(self, event: str, data: Dict):
        """Emit mock event for testing"""
        if event in self.event_handlers:
            for handler in self.event_handlers[event]:
                await handler(data)

class CDPPerformanceMonitor:
    """
    Advanced performance monitoring using Chrome DevTools Protocol
    """
    
    def __init__(self, cdp_session: MockCDPSession):
        self.cdp = cdp_session
        self.performance_data: List[PerformanceMetrics] = []
        self.network_requests: List[NetworkRequest] = []
        self.memory_snapshots: List[MemoryUsage] = []
        self.monitoring_active = False
    
    async def initialize(self):
        """Initialize CDP domains and event listeners"""
        try:
            # Enable required CDP domains
            await self.cdp.send("Performance.enable")
            await self.cdp.send("Network.enable")
            await self.cdp.send("Runtime.enable")
            await self.cdp.send("Memory.enable")
            
            # Set up event listeners
            self.cdp.on("Network.requestWillBeSent", self._handle_network_request)
            self.cdp.on("Network.responseReceived", self._handle_network_response)
            self.cdp.on("Performance.metrics", self._handle_performance_metrics)
            
            logger.info("CDP Performance Monitor initialized")
            
        except Exception as e:
            logger.error(f"Error initializing CDP monitor: {str(e)}")
    
    async def start_monitoring(self):
        """Start performance monitoring"""
        self.monitoring_active = True
        logger.info("Performance monitoring started")
        
        # Start periodic memory monitoring
        asyncio.create_task(self._monitor_memory_usage())
    
    async def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring_active = False
        logger.info("Performance monitoring stopped")
    
    async def _handle_network_request(self, event_data: Dict):
        """Handle network request events"""
        try:
            request = event_data.get("request", {})
            network_request = NetworkRequest(
                request_id=event_data.get("requestId", ""),
                url=request.get("url", ""),
                method=request.get("method", "GET"),
                status_code=0,  # Will be updated on response
                response_time=0,
                response_size=0,
                request_headers=request.get("headers", {}),
                response_headers={},
                timestamp=time.time()
            )
            
            self.network_requests.append(network_request)
            
        except Exception as e:
            logger.error(f"Error handling network request: {str(e)}")
    
    async def _handle_network_response(self, event_data: Dict):
        """Handle network response events"""
        try:
            request_id = event_data.get("requestId", "")
            response = event_data.get("response", {})
            
            # Find corresponding request
            for req in self.network_requests:
                if req.request_id == request_id:
                    req.status_code = response.get("status", 0)
                    req.response_headers = response.get("headers", {})
                    req.response_time = time.time() - req.timestamp
                    break
                    
        except Exception as e:
            logger.error(f"Error handling network response: {str(e)}")
    
    async def _handle_performance_metrics(self, event_data: Dict):
        """Handle performance metrics events"""
        try:
            metrics = event_data.get("metrics", [])
            
            # Parse metrics into structured format
            metric_values = {}
            for metric in metrics:
                metric_values[metric["name"]] = metric["value"]
            
            performance_metrics = PerformanceMetrics(
                navigation_start=metric_values.get("NavigationStart", 0),
                dom_content_loaded=metric_values.get("DOMContentLoaded", 0),
                load_complete=metric_values.get("LoadEventEnd", 0),
                first_paint=metric_values.get("FirstPaint", 0),
                first_contentful_paint=metric_values.get("FirstContentfulPaint", 0),
                largest_contentful_paint=metric_values.get("LargestContentfulPaint", 0),
                cumulative_layout_shift=metric_values.get("CumulativeLayoutShift", 0),
                first_input_delay=metric_values.get("FirstInputDelay", 0),
                total_blocking_time=metric_values.get("TotalBlockingTime", 0)
            )
            
            self.performance_data.append(performance_metrics)
            
        except Exception as e:
            logger.error(f"Error handling performance metrics: {str(e)}")
    
    async def _monitor_memory_usage(self):
        """Continuously monitor memory usage"""
        while self.monitoring_active:
            try:
                # Get JavaScript heap usage
                result = await self.cdp.send("Runtime.evaluate", {
                    "expression": "performance.memory",
                    "returnByValue": True
                })
                
                if "result" in result and "value" in result["result"]:
                    memory_info = result["result"]["value"]
                    
                    memory_usage = MemoryUsage(
                        used_js_heap_size=memory_info.get("usedJSHeapSize", 0),
                        total_js_heap_size=memory_info.get("totalJSHeapSize", 0),
                        js_heap_size_limit=memory_info.get("jsHeapSizeLimit", 0),
                        timestamp=time.time()
                    )
                    
                    self.memory_snapshots.append(memory_usage)
                
                # Wait before next measurement
                await asyncio.sleep(5)
                
            except Exception as e:
                logger.error(f"Error monitoring memory: {str(e)}")
                await asyncio.sleep(5)
    
    async def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        try:
            if not self.performance_data:
                return {"error": "No performance data available"}
            
            latest_metrics = self.performance_data[-1]
            
            # Calculate derived metrics
            page_load_time = latest_metrics.load_complete - latest_metrics.navigation_start
            dom_ready_time = latest_metrics.dom_content_loaded - latest_metrics.navigation_start
            
            # Network analysis
            total_requests = len(self.network_requests)
            failed_requests = sum(1 for req in self.network_requests if req.status_code >= 400)
            avg_response_time = sum(req.response_time for req in self.network_requests) / max(total_requests, 1)
            
            # Memory analysis
            if self.memory_snapshots:
                latest_memory = self.memory_snapshots[-1]
                memory_usage_mb = latest_memory.used_js_heap_size / (1024 * 1024)
            else:
                memory_usage_mb = 0
            
            report = {
                "performance_metrics": {
                    "page_load_time_ms": page_load_time,
                    "dom_ready_time_ms": dom_ready_time,
                    "first_contentful_paint_ms": latest_metrics.first_contentful_paint,
                    "largest_contentful_paint_ms": latest_metrics.largest_contentful_paint,
                    "cumulative_layout_shift": latest_metrics.cumulative_layout_shift,
                    "first_input_delay_ms": latest_metrics.first_input_delay
                },
                "network_analysis": {
                    "total_requests": total_requests,
                    "failed_requests": failed_requests,
                    "success_rate": ((total_requests - failed_requests) / max(total_requests, 1)) * 100,
                    "average_response_time_ms": avg_response_time * 1000
                },
                "memory_usage": {
                    "current_usage_mb": memory_usage_mb,
                    "heap_size_limit_mb": (latest_memory.js_heap_size_limit / (1024 * 1024)) if self.memory_snapshots else 0
                },
                "recommendations": self._generate_recommendations(latest_metrics, total_requests, failed_requests)
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating performance report: {str(e)}")
            return {"error": str(e)}
    
    def _generate_recommendations(self, metrics: PerformanceMetrics, total_requests: int, failed_requests: int) -> List[str]:
        """Generate performance optimization recommendations"""
        recommendations = []
        
        # Page load time recommendations
        page_load_time = metrics.load_complete - metrics.navigation_start
        if page_load_time > 3000:  # 3 seconds
            recommendations.append("Page load time is slow. Consider optimizing images and reducing bundle size.")
        
        # LCP recommendations
        if metrics.largest_contentful_paint > 2500:  # 2.5 seconds
            recommendations.append("Largest Contentful Paint is slow. Optimize critical rendering path.")
        
        # CLS recommendations
        if metrics.cumulative_layout_shift > 0.1:
            recommendations.append("High Cumulative Layout Shift detected. Ensure proper sizing for dynamic content.")
        
        # Network recommendations
        if failed_requests > 0:
            recommendations.append(f"{failed_requests} network requests failed. Check for broken links or API issues.")
        
        if total_requests > 50:
            recommendations.append("High number of network requests. Consider bundling resources or using HTTP/2.")
        
        return recommendations

class CDPDebugger:
    """
    Advanced JavaScript debugging using CDP
    """
    
    def __init__(self, cdp_session: MockCDPSession):
        self.cdp = cdp_session
        self.breakpoints: List[Dict] = []
        self.console_logs: List[Dict] = []
        self.exceptions: List[Dict] = []
    
    async def initialize(self):
        """Initialize debugging capabilities"""
        await self.cdp.send("Debugger.enable")
        await self.cdp.send("Runtime.enable")
        await self.cdp.send("Console.enable")
        
        # Set up event listeners
        self.cdp.on("Console.messageAdded", self._handle_console_message)
        self.cdp.on("Runtime.exceptionThrown", self._handle_exception)
        
        logger.info("CDP Debugger initialized")
    
    async def set_breakpoint(self, url: str, line_number: int, condition: str = None) -> str:
        """Set a breakpoint in JavaScript code"""
        try:
            params = {
                "lineNumber": line_number,
                "url": url
            }
            
            if condition:
                params["condition"] = condition
            
            result = await self.cdp.send("Debugger.setBreakpointByUrl", params)
            breakpoint_id = result.get("breakpointId", "")
            
            self.breakpoints.append({
                "id": breakpoint_id,
                "url": url,
                "line": line_number,
                "condition": condition
            })
            
            logger.info(f"Breakpoint set: {url}:{line_number}")
            return breakpoint_id
            
        except Exception as e:
            logger.error(f"Error setting breakpoint: {str(e)}")
            return ""
    
    async def evaluate_expression(self, expression: str, context_id: int = None) -> Dict[str, Any]:
        """Evaluate JavaScript expression in browser context"""
        try:
            params = {
                "expression": expression,
                "returnByValue": True
            }
            
            if context_id:
                params["contextId"] = context_id
            
            result = await self.cdp.send("Runtime.evaluate", params)
            return result
            
        except Exception as e:
            logger.error(f"Error evaluating expression: {str(e)}")
            return {"error": str(e)}
    
    async def _handle_console_message(self, event_data: Dict):
        """Handle console messages"""
        self.console_logs.append({
            "level": event_data.get("level", "log"),
            "text": event_data.get("text", ""),
            "timestamp": time.time()
        })
    
    async def _handle_exception(self, event_data: Dict):
        """Handle JavaScript exceptions"""
        exception_details = event_data.get("exceptionDetails", {})
        self.exceptions.append({
            "message": exception_details.get("text", ""),
            "line": exception_details.get("lineNumber", 0),
            "column": exception_details.get("columnNumber", 0),
            "url": exception_details.get("url", ""),
            "timestamp": time.time()
        })
    
    def get_debug_summary(self) -> Dict[str, Any]:
        """Get debugging session summary"""
        return {
            "breakpoints_set": len(self.breakpoints),
            "console_messages": len(self.console_logs),
            "exceptions_caught": len(self.exceptions),
            "recent_logs": self.console_logs[-10:],  # Last 10 logs
            "recent_exceptions": self.exceptions[-5:]  # Last 5 exceptions
        }

# Example usage and demonstrations
async def demo_performance_monitoring():
    """Demonstrate CDP performance monitoring"""
    cdp_session = MockCDPSession()
    monitor = CDPPerformanceMonitor(cdp_session)
    
    try:
        await monitor.initialize()
        await monitor.start_monitoring()
        
        # Simulate some activity
        await asyncio.sleep(2)
        
        # Emit mock events for demonstration
        await cdp_session.emit_mock_event("Network.requestWillBeSent", {
            "requestId": "req1",
            "request": {
                "url": "https://example.com/api/data",
                "method": "GET",
                "headers": {"User-Agent": "Test"}
            }
        })
        
        await cdp_session.emit_mock_event("Performance.metrics", {
            "metrics": [
                {"name": "NavigationStart", "value": time.time() * 1000},
                {"name": "DOMContentLoaded", "value": time.time() * 1000 + 500},
                {"name": "LoadEventEnd", "value": time.time() * 1000 + 1000},
                {"name": "FirstContentfulPaint", "value": time.time() * 1000 + 800}
            ]
        })
        
        await asyncio.sleep(1)
        await monitor.stop_monitoring()
        
        # Generate performance report
        report = await monitor.get_performance_report()
        
        # Save report to file
        with open("performance_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print("Performance monitoring demo completed!")
        print(f"Report saved with {len(monitor.performance_data)} performance snapshots")
        
    except Exception as e:
        logger.error(f"Demo error: {str(e)}")

async def demo_debugging_capabilities():
    """Demonstrate CDP debugging features"""
    cdp_session = MockCDPSession()
    debugger = CDPDebugger(cdp_session)
    
    try:
        await debugger.initialize()
        
        # Set some breakpoints
        await debugger.set_breakpoint("https://example.com/app.js", 25, "user.id === 123")
        await debugger.set_breakpoint("https://example.com/utils.js", 10)
        
        # Evaluate some expressions
        result1 = await debugger.evaluate_expression("document.title")
        result2 = await debugger.evaluate_expression("window.location.href")
        
        # Simulate console messages and exceptions
        await cdp_session.emit_mock_event("Console.messageAdded", {
            "level": "error",
            "text": "Failed to load resource"
        })
        
        await cdp_session.emit_mock_event("Runtime.exceptionThrown", {
            "exceptionDetails": {
                "text": "TypeError: Cannot read property 'id' of undefined",
                "lineNumber": 42,
                "columnNumber": 15,
                "url": "https://example.com/app.js"
            }
        })
        
        # Get debugging summary
        summary = debugger.get_debug_summary()
        
        print("Debugging demo completed!")
        print(f"Breakpoints set: {summary['breakpoints_set']}")
        print(f"Console messages: {summary['console_messages']}")
        print(f"Exceptions caught: {summary['exceptions_caught']}")
        
    except Exception as e:
        logger.error(f"Demo error: {str(e)}")

if __name__ == "__main__":
    print("Chrome DevTools Protocol Integration Demo")
    print("=" * 45)
    
    # Run demonstrations
    asyncio.run(demo_performance_monitoring())
    asyncio.run(demo_debugging_capabilities())
