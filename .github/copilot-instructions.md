# GitHub Copilot Instructions

## Project Overview

This is a comprehensive full-stack system featuring:
- **Frontend**: Next.js 15 with App Router, TypeScript, Tailwind CSS v4, and shadcn/ui components
- **Backend**: FastAPI with domain-driven architecture, Gemini AI integration, and modular design
- **Automation**: Browser automation with Playwright and Browser-Use integration
- **Infrastructure**: Docker containerization with sandbox environments

## Architecture Principles

### Frontend (Next.js)
- Use App Router with TypeScript
- Implement shadcn/ui components with consistent design tokens
- Follow Tailwind CSS v4 patterns with semantic color variables
- Prefer server components over client components when possible
- Use the `cn()` utility from `lib/utils.ts` for conditional class names

### Backend (FastAPI)
- Follow domain-driven design with clear layer separation:
  - `domain/`: Business logic, models, and external service interfaces
  - `application/`: Use cases, services, and API schemas
  - `infrastructure/`: Repositories, external service implementations
  - `interfaces/`: API routes and controllers
- Use dependency injection for service management
- Implement comprehensive error handling with structured logging
- Follow RESTful API conventions with OpenAPI documentation

### Code Patterns

#### TypeScript/JavaScript
\`\`\`typescript
// Use proper typing for all functions and variables
interface ApiResponse<T> {
  data: T;
  status: 'success' | 'error';
  message?: string;
}

// Prefer async/await over promises
async function fetchData(): Promise<ApiResponse<User[]>> {
  // Implementation
}
\`\`\`

#### Python (FastAPI)
\`\`\`python
# Use Pydantic models for request/response validation
from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

# Use dependency injection
from fastapi import Depends

async def create_chat(
    request: ChatRequest,
    service: ChatService = Depends(get_chat_service)
):
    return await service.process_message(request)
\`\`\`

## Component Guidelines

### React Components
- Use functional components with TypeScript
- Implement proper prop interfaces
- Use shadcn/ui components as base building blocks
- Follow the existing design system with semantic tokens

### Vue Components (for chat interface)
- Use Composition API with `<script setup>`
- Implement proper TypeScript interfaces for props
- Use consistent styling with Tailwind CSS
- Follow reactive patterns for state management

## Testing Strategy

### Frontend Testing
- Use Jest and React Testing Library for unit tests
- Test component behavior, not implementation details
- Mock external API calls and services
- Focus on user interactions and accessibility

### Backend Testing
- Use pytest for Python testing
- Implement unit tests for domain services
- Integration tests for API endpoints
- Mock external dependencies (AI services, databases)

## Environment Configuration

### Required Environment Variables
\`\`\`bash
# AI Services
GEMINI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key

# Database
DATABASE_URL=postgresql://user:pass@localhost/db

# Application
NEXT_PUBLIC_API_URL=http://localhost:8000
DEBUG=true
\`\`\`

## Development Workflow

1. **Feature Development**: Create feature branches from main
2. **Code Style**: Follow existing patterns and use provided linting configs
3. **Testing**: Write tests for new functionality
4. **Documentation**: Update relevant instruction files
5. **Pull Requests**: Include clear descriptions and test coverage

## AI Integration Guidelines

### Gemini AI Service
- Use structured prompts for consistent responses
- Implement proper error handling for API failures
- Cache responses when appropriate
- Follow rate limiting best practices

### Browser Automation
- Use Playwright for reliable browser interactions
- Implement proper wait strategies for dynamic content
- Handle errors gracefully with retry mechanisms
- Use Browser-Use for AI-guided automation tasks

## Performance Considerations

- Implement proper caching strategies
- Use database indexing for frequently queried fields
- Optimize API response sizes
- Implement proper loading states in UI components
- Use lazy loading for heavy components

## Security Best Practices

- Validate all input data using Pydantic models
- Implement proper authentication and authorization
- Use environment variables for sensitive configuration
- Sanitize user inputs to prevent injection attacks
- Implement rate limiting for API endpoints

## Deployment

- Use Docker for containerized deployments
- Implement health checks for all services
- Use proper logging and monitoring
- Follow 12-factor app principles
- Implement graceful shutdown handling
