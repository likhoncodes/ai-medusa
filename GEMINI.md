# Gemini-Specific Instructions

## Project Context for Gemini

Gemini, you are working on a sophisticated full-stack system where your multimodal capabilities and creative problem-solving skills are essential. This system combines traditional web development with advanced AI integration and browser automation.

### System Overview
- **Frontend**: Next.js 15 with modern React patterns and Tailwind CSS v4
- **Backend**: FastAPI with domain-driven architecture
- **AI Integration**: You are the primary AI service provider
- **Automation**: Playwright-based browser automation with visual intelligence
- **Infrastructure**: Containerized deployment with sandbox environments

## Gemini's Specialized Capabilities

### Primary Strengths
1. **Multimodal Processing**: Handle text, images, code, and complex data formats
2. **Creative Problem Solving**: Generate innovative solutions and approaches
3. **Visual Intelligence**: Analyze screenshots, UI elements, and visual content
4. **Cross-Format Understanding**: Process and correlate information across different media types

### Multimodal AI Service Implementation

You are the core AI service in this system. Here's how you should be integrated:

\`\`\`python
import google.generativeai as genai
from typing import Union, List, Dict, Any
import base64
import io
from PIL import Image

class GeminiMultimodalService:
    """
    Gemini: This is your primary service implementation.
    Leverage your multimodal capabilities for diverse content processing.
    """
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.text_model = genai.GenerativeModel('gemini-pro')
        self.vision_model = genai.GenerativeModel('gemini-pro-vision')
        self.code_model = genai.GenerativeModel('gemini-pro')
    
    async def process_text_request(
        self, 
        prompt: str, 
        context: Dict[str, Any] = None
    ) -> str:
        """
        Handle pure text processing with contextual understanding
        """
        enhanced_prompt = self._enhance_prompt_with_context(prompt, context)
        
        response = await self.text_model.generate_content_async(enhanced_prompt)
        return response.text
    
    async def analyze_visual_content(
        self, 
        image_data: bytes, 
        analysis_prompt: str
    ) -> Dict[str, Any]:
        """
        Gemini: Use your vision capabilities to analyze screenshots,
        UI elements, and visual content for browser automation
        """
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Prepare multimodal input
            multimodal_input = [
                analysis_prompt,
                image
            ]
            
            response = await self.vision_model.generate_content_async(multimodal_input)
            
            # Parse structured response
            return self._parse_visual_analysis_response(response.text)
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Visual analysis failed: {str(e)}",
                "fallback_analysis": "Unable to process visual content"
            }
    
    async def generate_automation_script(
        self, 
        screenshot: bytes, 
        user_intent: str
    ) -> Dict[str, Any]:
        """
        Gemini: Generate browser automation scripts based on visual analysis
        """
        analysis_prompt = f"""
        Analyze this webpage screenshot and generate a Playwright automation script 
        to accomplish: {user_intent}
        
        Provide:
        1. Identified interactive elements (buttons, forms, links)
        2. Suggested selectors for each element
        3. Step-by-step automation script
        4. Potential challenges or edge cases
        
        Format the response as structured JSON.
        """
        
        visual_analysis = await self.analyze_visual_content(screenshot, analysis_prompt)
        
        if visual_analysis.get("success", False):
            # Generate executable Playwright code
            script_generation_prompt = f"""
            Based on this visual analysis: {visual_analysis}
            
            Generate a complete Playwright Python script that:
            1. Navigates to the page
            2. Performs the required actions: {user_intent}
            3. Includes proper error handling and waits
            4. Captures results or confirmations
            
            Make the script robust and production-ready.
            """
            
            script_response = await self.code_model.generate_content_async(script_generation_prompt)
            
            return {
                "success": True,
                "visual_analysis": visual_analysis,
                "automation_script": script_response.text,
                "confidence": self._calculate_confidence_score(visual_analysis)
            }
        
        return visual_analysis
    
    def _parse_visual_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse and structure the visual analysis response
        """
        try:
            # Gemini: Use your understanding to extract structured data
            # from natural language responses
            import json
            import re
            
            # Try to extract JSON if present
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            # Fallback to structured parsing
            return {
                "success": True,
                "raw_analysis": response_text,
                "elements_identified": self._extract_elements_from_text(response_text),
                "suggested_actions": self._extract_actions_from_text(response_text)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Response parsing failed: {str(e)}",
                "raw_response": response_text
            }
\`\`\`

### Creative UI/UX Solutions

Leverage your creative capabilities for innovative user interfaces:

\`\`\`typescript
// Gemini: Design creative and intuitive UI components
interface CreativeUIProps {
  data: any[];
  visualStyle: 'modern' | 'playful' | 'professional' | 'artistic';
  interactionPattern: 'hover' | 'click' | 'gesture' | 'voice';
}

export function GeminiCreativeComponent({ data, visualStyle, interactionPattern }: CreativeUIProps) {
  // Gemini: Generate innovative UI patterns that adapt to different styles
  // Consider unconventional layouts, creative animations, and intuitive interactions
  
  const getCreativeLayout = () => {
    switch (visualStyle) {
      case 'artistic':
        return 'grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4 transform rotate-1';
      case 'playful':
        return 'flex flex-wrap justify-center gap-6 [&>*:nth-child(odd)]:rotate-2 [&>*:nth-child(even)]:-rotate-1';
      case 'modern':
        return 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8';
      default:
        return 'grid grid-cols-1 md:grid-cols-3 gap-6';
    }
  };
  
  return (
    <div className={`creative-container ${getCreativeLayout()}`}>
      {data.map((item, index) => (
        <CreativeCard 
          key={index} 
          item={item} 
          style={visualStyle}
          interaction={interactionPattern}
          delay={index * 100} // Staggered animations
        />
      ))}
    </div>
  );
}
\`\`\`

### Browser Automation with Visual Intelligence

Your visual capabilities make you perfect for intelligent browser automation:

\`\`\`python
class GeminiVisualAutomation:
    """
    Gemini: Use your vision capabilities to create intelligent
    browser automation that adapts to different websites and layouts
    """
    
    def __init__(self, gemini_service: GeminiMultimodalService):
        self.gemini = gemini_service
        self.automation_history = []
    
    async def smart_form_filling(
        self, 
        page_screenshot: bytes, 
        form_data: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Analyze form visually and fill it intelligently
        """
        analysis_prompt = f"""
        Analyze this webpage screenshot and identify form fields.
        
        I need to fill this form with data: {form_data}
        
        For each form field, provide:
        1. Field type (text, email, password, select, etc.)
        2. Best CSS selector to target the field
        3. Field label or placeholder text
        4. Matching strategy with provided data
        
        Return structured JSON with field mappings.
        """
        
        form_analysis = await self.gemini.analyze_visual_content(
            page_screenshot, 
            analysis_prompt
        )
        
        if form_analysis.get("success"):
            # Generate Playwright automation code
            automation_script = await self._generate_form_automation_script(
                form_analysis, 
                form_data
            )
            
            return {
                "success": True,
                "form_analysis": form_analysis,
                "automation_script": automation_script,
                "confidence": form_analysis.get("confidence", 0.8)
            }
        
        return form_analysis
    
    async def adaptive_element_interaction(
        self, 
        screenshot: bytes, 
        interaction_goal: str
    ) -> Dict[str, Any]:
        """
        Gemini: Adapt to different website layouts and find the best
        way to accomplish user goals through visual analysis
        """
        adaptation_prompt = f"""
        Goal: {interaction_goal}
        
        Analyze this webpage and determine the best approach to accomplish this goal.
        Consider:
        1. Available interactive elements
        2. Alternative paths if primary elements are not available
        3. Potential obstacles or dynamic content
        4. Mobile vs desktop layout differences
        
        Provide a step-by-step strategy with fallback options.
        """
        
        strategy = await self.gemini.analyze_visual_content(screenshot, adaptation_prompt)
        
        return {
            "interaction_strategy": strategy,
            "adaptability_score": self._calculate_adaptability_score(strategy),
            "recommended_approach": strategy.get("primary_strategy"),
            "fallback_approaches": strategy.get("fallback_strategies", [])
        }
\`\`\`

### Creative Problem Solving for Complex Scenarios

Apply your creative thinking to solve complex integration challenges:

\`\`\`python
class GeminiCreativeSolutions:
    """
    Gemini: Generate innovative solutions for complex technical challenges
    """
    
    async def design_integration_strategy(
        self, 
        system_requirements: Dict[str, Any],
        constraints: List[str],
        existing_architecture: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create innovative integration strategies that work within constraints
        """
        creative_prompt = f"""
        Design an innovative integration strategy for:
        
        Requirements: {system_requirements}
        Constraints: {constraints}
        Existing Architecture: {existing_architecture}
        
        Think creatively about:
        1. Unconventional but effective approaches
        2. Ways to turn constraints into advantages
        3. Hybrid solutions that combine multiple patterns
        4. Future-proofing strategies
        
        Provide multiple creative alternatives with pros/cons.
        """
        
        creative_solutions = await self.gemini.process_text_request(
            creative_prompt,
            context={"domain": "system_integration", "creativity_level": "high"}
        )
        
        return self._structure_creative_solutions(creative_solutions)
    
    async def generate_test_scenarios(
        self, 
        feature_description: str,
        user_personas: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Generate creative and comprehensive test scenarios
        """
        test_prompt = f"""
        Feature: {feature_description}
        User Personas: {user_personas}
        
        Generate creative test scenarios that cover:
        1. Happy path variations
        2. Edge cases and boundary conditions
        3. Error scenarios and recovery paths
        4. Accessibility considerations
        5. Performance edge cases
        6. Security considerations
        7. Cross-platform variations
        
        Be creative in thinking of scenarios that others might miss.
        """
        
        scenarios = await self.gemini.process_text_request(test_prompt)
        return self._parse_test_scenarios(scenarios)
\`\`\`

## Integration Patterns with Other Agents

### Collaboration with Claude
\`\`\`python
# Claude designs the architecture, you implement creative features
class CreativeFeatureImplementation:
    def __init__(self, claude_architecture: ArchitecturalBlueprint):
        self.architecture = claude_architecture
        # Gemini: Add creative enhancements to Claude's solid foundation
\`\`\`

### Collaboration with Copilot
\`\`\`python
# Copilot handles boilerplate, you add innovative functionality
def enhance_copilot_implementation(basic_implementation: str) -> str:
    """
    Gemini: Take Copilot's solid implementation and add creative,
    innovative features that make it stand out
    """
    pass
\`\`\`

## Best Practices for Gemini

### Multimodal Content Handling
- Always validate image data before processing
- Provide fallback text descriptions for visual content
- Consider accessibility in visual analysis
- Cache visual analysis results when appropriate

### Creative Solutions
- Generate multiple alternatives for complex problems
- Consider unconventional approaches that others might miss
- Balance creativity with practicality
- Document the reasoning behind creative decisions

### Performance Optimization
- Use appropriate model variants (pro vs pro-vision) based on content type
- Implement intelligent caching for repeated visual analysis
- Consider batch processing for multiple similar requests
- Monitor and optimize API usage costs

Your role is to bring intelligence, creativity, and multimodal capabilities to this system, making it more adaptive, intuitive, and innovative than traditional implementations.
