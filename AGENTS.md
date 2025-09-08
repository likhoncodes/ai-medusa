# AI Coding Agents Guide

## Overview
This document provides specific instructions for different AI coding agents working on this project. Each agent has unique capabilities that should be leveraged appropriately.

## GitHub Copilot

### Strengths
- Excellent at code completion and pattern recognition
- Strong understanding of common frameworks and libraries
- Good at generating boilerplate code and tests

### Best Use Cases
- Auto-completing function implementations
- Generating test cases based on existing patterns
- Creating API endpoint boilerplate
- Implementing common design patterns

### Configuration
- Uses the instructions in `.github/copilot-instructions.md`
- Follows established code patterns in the repository
- Leverages context from open files and recent changes

## Claude (Anthropic)

### Strengths
- Excellent at architectural decisions and code organization
- Strong analytical capabilities for complex problems
- Good at explaining code and writing documentation
- Excellent at refactoring and code optimization

### Best Use Cases
- System architecture design and review
- Complex algorithm implementation
- Code refactoring and optimization
- Technical documentation writing
- Error analysis and debugging

### Usage Guidelines
\`\`\`python
# Claude excels at complex business logic
class ChatOrchestrator:
    """
    Claude is particularly good at designing services that coordinate
    multiple components with complex business rules.
    """
    
    async def orchestrate_conversation(
        self, 
        user_input: str, 
        context: ConversationContext
    ) -> ConversationResponse:
        # Complex orchestration logic that Claude handles well
        pass
\`\`\`

## Gemini (Google)

### Strengths
- Excellent multimodal capabilities (text, images, code)
- Strong at creative problem solving
- Good at generating diverse solutions
- Excellent at understanding context across different file types

### Best Use Cases
- Image processing and analysis tasks
- Creative UI/UX implementations
- Multi-format data processing
- Cross-platform integration solutions
- Browser automation with visual elements

### Integration Examples
\`\`\`python
# Gemini excels at multimodal tasks
class VisualAutomationAgent:
    def __init__(self):
        self.gemini_client = genai.GenerativeModel('gemini-pro-vision')
    
    async def analyze_screenshot_and_act(self, screenshot: bytes, instruction: str):
        """
        Gemini can analyze screenshots and provide intelligent
        automation instructions based on visual content
        """
        response = await self.gemini_client.generate_content([
            f"Analyze this screenshot and {instruction}",
            {"mime_type": "image/png", "data": screenshot}
        ])
        return response.text
\`\`\`

## Agent Collaboration Patterns

### Sequential Processing
\`\`\`python
# 1. Copilot generates boilerplate
async def process_user_request(request: UserRequest):
    # Copilot: Generate basic structure
    pass

# 2. Claude optimizes architecture
class RequestProcessor:
    # Claude: Design optimal service architecture
    pass

# 3. Gemini handles multimodal aspects
async def handle_visual_content(content: VisualContent):
    # Gemini: Process images, videos, complex formats
    pass
\`\`\`

### Parallel Specialization
- **Copilot**: Handle routine code completion and testing
- **Claude**: Focus on architecture and complex business logic
- **Gemini**: Manage multimodal features and creative solutions

### Code Review Workflow
1. **Copilot**: Initial code generation and completion
2. **Claude**: Architecture review and optimization suggestions
3. **Gemini**: Creative alternatives and multimodal integration review

## Agent-Specific Prompting

### For Copilot
\`\`\`typescript
// Clear, specific function signatures work best
interface UserService {
  createUser(userData: CreateUserRequest): Promise<User>;
  updateUser(id: string, updates: UpdateUserRequest): Promise<User>;
  deleteUser(id: string): Promise<void>;
}
\`\`\`

### For Claude
\`\`\`python
"""
Provide detailed context and requirements for Claude:

Requirements:
- Implement domain-driven design principles
- Ensure proper error handling and logging
- Consider scalability and maintainability
- Follow SOLID principles

Context:
- This service coordinates between multiple external APIs
- Must handle high concurrency and rate limiting
- Needs comprehensive audit logging
"""
class ComplexOrchestrationService:
    pass
\`\`\`

### For Gemini
\`\`\`python
"""
Leverage Gemini's multimodal capabilities:

Task: Create a browser automation system that can:
- Analyze webpage screenshots
- Identify interactive elements visually
- Generate automation scripts based on visual analysis
- Handle dynamic content and responsive layouts
"""
class VisualBrowserAutomation:
    pass
\`\`\`

## Best Practices

### Agent Selection Guidelines
- **Simple CRUD operations**: Copilot
- **Complex business logic**: Claude
- **Multimodal features**: Gemini
- **Architecture decisions**: Claude
- **Creative UI solutions**: Gemini
- **Test generation**: Copilot

### Collaboration Workflow
1. Start with architectural planning (Claude)
2. Generate implementation boilerplate (Copilot)
3. Add multimodal features (Gemini)
4. Optimize and refactor (Claude)
5. Complete testing (Copilot)

### Quality Assurance
- Each agent should review code generated by others
- Use agent strengths for specialized code reviews
- Maintain consistency across agent-generated code
- Document agent contributions for future reference
