"""
Comprehensive Playwright Integration Examples
============================================

This script demonstrates various Playwright integration examples focusing on:
- Custom actions for form filling
- Screenshot capturing with different strategies
- Text extraction and content analysis
- Advanced browser automation patterns
"""

import asyncio
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PlaywrightAutomation:
    """
    Advanced Playwright automation class with custom actions
    """
    
    def __init__(self, headless: bool = True, slow_mo: int = 0):
        self.headless = headless
        self.slow_mo = slow_mo
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
    async def initialize(self):
        """Initialize browser, context, and page"""
        playwright = await async_playwright().start()
        
        # Launch browser with custom configuration
        self.browser = await playwright.chromium.launch(
            headless=self.headless,
            slow_mo=self.slow_mo,
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-blink-features=AutomationControlled'
            ]
        )
        
        # Create context with realistic user agent and viewport
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        # Create page and set up event listeners
        self.page = await self.context.new_page()
        await self._setup_page_listeners()
        
        logger.info("Playwright automation initialized successfully")
    
    async def _setup_page_listeners(self):
        """Set up page event listeners for monitoring"""
        if not self.page:
            return
            
        self.page.on("console", lambda msg: logger.info(f"Console: {msg.text}"))
        self.page.on("pageerror", lambda error: logger.error(f"Page error: {error}"))
        self.page.on("requestfailed", lambda request: logger.warning(f"Request failed: {request.url}"))
    
    async def smart_form_fill(self, form_data: Dict[str, Any], form_selector: str = "form") -> bool:
        """
        Advanced form filling with intelligent field detection
        
        Args:
            form_data: Dictionary containing field names/labels and their values
            form_selector: CSS selector for the form container
            
        Returns:
            bool: Success status of form filling
        """
        try:
            if not self.page:
                raise Exception("Page not initialized")
            
            # Wait for form to be visible
            await self.page.wait_for_selector(form_selector, timeout=10000)
            
            # Get all form fields
            form_fields = await self.page.query_selector_all(f"{form_selector} input, {form_selector} textarea, {form_selector} select")
            
            filled_fields = 0
            
            for field_name, field_value in form_data.items():
                field_filled = False
                
                # Try different strategies to find and fill the field
                strategies = [
                    f"input[name='{field_name}']",
                    f"input[id='{field_name}']",
                    f"textarea[name='{field_name}']",
                    f"select[name='{field_name}']",
                    f"input[placeholder*='{field_name}' i]",
                    f"label:has-text('{field_name}') + input",
                    f"label:has-text('{field_name}') input"
                ]
                
                for strategy in strategies:
                    try:
                        element = await self.page.query_selector(strategy)
                        if element:
                            # Check element type and fill accordingly
                            tag_name = await element.evaluate("el => el.tagName.toLowerCase()")
                            element_type = await element.evaluate("el => el.type || ''")
                            
                            if tag_name == "select":
                                await element.select_option(str(field_value))
                            elif element_type in ["checkbox", "radio"]:
                                if field_value:
                                    await element.check()
                                else:
                                    await element.uncheck()
                            else:
                                await element.clear()
                                await element.fill(str(field_value))
                            
                            filled_fields += 1
                            field_filled = True
                            logger.info(f"Successfully filled field: {field_name}")
                            break
                            
                    except Exception as e:
                        continue
                
                if not field_filled:
                    logger.warning(f"Could not fill field: {field_name}")
            
            logger.info(f"Form filling completed. Filled {filled_fields}/{len(form_data)} fields")
            return filled_fields > 0
            
        except Exception as e:
            logger.error(f"Error in smart_form_fill: {str(e)}")
            return False
    
    async def capture_screenshot_with_options(self, 
                                            filename: str,
                                            full_page: bool = False,
                                            element_selector: Optional[str] = None,
                                            mask_selectors: List[str] = None) -> str:
        """
        Advanced screenshot capture with multiple options
        
        Args:
            filename: Output filename for the screenshot
            full_page: Whether to capture the full page
            element_selector: Specific element to screenshot
            mask_selectors: List of selectors to mask in the screenshot
            
        Returns:
            str: Path to the saved screenshot
        """
        try:
            if not self.page:
                raise Exception("Page not initialized")
            
            # Ensure screenshots directory exists
            screenshots_dir = Path("screenshots")
            screenshots_dir.mkdir(exist_ok=True)
            
            screenshot_path = screenshots_dir / filename
            
            screenshot_options = {
                "path": str(screenshot_path),
                "type": "png"
            }
            
            # Apply masking if specified
            if mask_selectors:
                for selector in mask_selectors:
                    try:
                        await self.page.add_style_tag(content=f"""
                            {selector} {{
                                background: #000000 !important;
                                color: transparent !important;
                            }}
                        """)
                    except:
                        pass
            
            # Take screenshot based on options
            if element_selector:
                element = await self.page.query_selector(element_selector)
                if element:
                    await element.screenshot(**screenshot_options)
                else:
                    logger.warning(f"Element not found: {element_selector}")
                    await self.page.screenshot(**screenshot_options)
            else:
                screenshot_options["full_page"] = full_page
                await self.page.screenshot(**screenshot_options)
            
            logger.info(f"Screenshot saved: {screenshot_path}")
            return str(screenshot_path)
            
        except Exception as e:
            logger.error(f"Error capturing screenshot: {str(e)}")
            return ""
    
    async def extract_structured_text(self, extraction_config: Dict[str, str]) -> Dict[str, Any]:
        """
        Extract structured text content based on configuration
        
        Args:
            extraction_config: Dictionary mapping field names to CSS selectors
            
        Returns:
            Dict containing extracted text data
        """
        try:
            if not self.page:
                raise Exception("Page not initialized")
            
            extracted_data = {}
            
            for field_name, selector in extraction_config.items():
                try:
                    # Handle different extraction types
                    if selector.startswith("@"):
                        # Special extraction commands
                        command = selector[1:]
                        if command == "title":
                            extracted_data[field_name] = await self.page.title()
                        elif command == "url":
                            extracted_data[field_name] = self.page.url
                        elif command == "html":
                            extracted_data[field_name] = await self.page.content()
                    else:
                        # Regular CSS selector extraction
                        elements = await self.page.query_selector_all(selector)
                        
                        if len(elements) == 1:
                            # Single element
                            text = await elements[0].text_content()
                            extracted_data[field_name] = text.strip() if text else ""
                        elif len(elements) > 1:
                            # Multiple elements - return as list
                            texts = []
                            for element in elements:
                                text = await element.text_content()
                                if text and text.strip():
                                    texts.append(text.strip())
                            extracted_data[field_name] = texts
                        else:
                            extracted_data[field_name] = None
                            
                except Exception as e:
                    logger.warning(f"Failed to extract {field_name}: {str(e)}")
                    extracted_data[field_name] = None
            
            logger.info(f"Text extraction completed for {len(extraction_config)} fields")
            return extracted_data
            
        except Exception as e:
            logger.error(f"Error in extract_structured_text: {str(e)}")
            return {}
    
    async def wait_for_network_idle(self, timeout: int = 30000, idle_time: int = 500):
        """Wait for network to be idle (no requests for specified time)"""
        try:
            await self.page.wait_for_load_state("networkidle", timeout=timeout)
            await asyncio.sleep(idle_time / 1000)  # Additional wait
            logger.info("Network idle state achieved")
        except Exception as e:
            logger.warning(f"Network idle wait failed: {str(e)}")
    
    async def close(self):
        """Clean up resources"""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        logger.info("Playwright automation closed")

# Example usage and demonstrations
async def demo_form_automation():
    """Demonstrate advanced form filling capabilities"""
    automation = PlaywrightAutomation(headless=False, slow_mo=1000)
    
    try:
        await automation.initialize()
        
        # Navigate to a form page (example)
        await automation.page.goto("https://httpbin.org/forms/post")
        
        # Define form data
        form_data = {
            "custname": "John Doe",
            "custtel": "555-1234",
            "custemail": "john@example.com",
            "size": "medium",
            "delivery": "19:00"
        }
        
        # Fill form using smart detection
        success = await automation.smart_form_fill(form_data)
        
        if success:
            # Take screenshot of filled form
            await automation.capture_screenshot_with_options(
                "filled_form.png",
                element_selector="form"
            )
            
            print("Form automation demo completed successfully!")
        
    except Exception as e:
        logger.error(f"Demo error: {str(e)}")
    finally:
        await automation.close()

async def demo_content_extraction():
    """Demonstrate structured content extraction"""
    automation = PlaywrightAutomation()
    
    try:
        await automation.initialize()
        
        # Navigate to a content-rich page
        await automation.page.goto("https://news.ycombinator.com")
        await automation.wait_for_network_idle()
        
        # Define extraction configuration
        extraction_config = {
            "title": "@title",
            "url": "@url",
            "headlines": ".titleline > a",
            "scores": ".score",
            "comments": ".subline a[href*='item']"
        }
        
        # Extract structured data
        extracted_data = await automation.extract_structured_text(extraction_config)
        
        # Save extracted data
        with open("extracted_data.json", "w") as f:
            json.dump(extracted_data, f, indent=2)
        
        # Take full page screenshot
        await automation.capture_screenshot_with_options(
            "hacker_news_full.png",
            full_page=True
        )
        
        print("Content extraction demo completed!")
        print(f"Extracted {len(extracted_data)} data fields")
        
    except Exception as e:
        logger.error(f"Demo error: {str(e)}")
    finally:
        await automation.close()

if __name__ == "__main__":
    print("Playwright Custom Actions Demo")
    print("=" * 40)
    
    # Run demonstrations
    asyncio.run(demo_form_automation())
    asyncio.run(demo_content_extraction())
