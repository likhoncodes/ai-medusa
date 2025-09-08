# 🐍 AI Medusa - Intelligent Automation Platform

> **AI-powered automation platform with browser control, multi-agent execution, and intelligent task processing**

[![GitHub](https://img.shields.io/badge/GitHub-likhoncodes%2Fai--medusa-blue?logo=github)](https://github.com/likhoncodes/ai-medusa)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Next.js](https://img.shields.io/badge/Next.js-15.1.3-black?logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Gemini AI](https://img.shields.io/badge/Gemini-AI-4285F4?logo=google)](https://ai.google.dev/)

## 🚀 Features

- **🤖 Multi-Agent AI**: Parallel execution with intelligent task distribution and coordination
- **🌐 Browser Automation**: Advanced Playwright integration for web scraping and form automation  
- **⚡ Gemini AI Integration**: Powered by Google's advanced Gemini model for intelligent processing
- **🔧 FastAPI Backend**: High-performance API with modular architecture and real-time processing
- **📊 Data Processing**: Advanced data transformation, normalization, aggregation, and validation
- **🔍 CDP Integration**: Chrome DevTools Protocol for debugging and performance monitoring
- **🛡️ Secure Sandbox**: Docker containerization with isolated execution environments
- **📚 OpenAPI Docs**: Comprehensive API documentation with interactive testing
- **🎯 TypeScript**: Full type safety and enhanced developer experience

## 🏗️ Architecture Overview

\`\`\`plaintext
ai-medusa/
├── 🎨 Frontend (Next.js + React)
│   ├── app/                    # Next.js App Router
│   ├── components/             # Reusable UI components
│   └── lib/                    # Utilities and services
├── 🚀 Backend (FastAPI)
│   ├── app/domain/            # Business logic layer
│   ├── app/application/       # Application services
│   ├── app/infrastructure/    # External integrations
│   └── app/interfaces/        # API routes
├── 🤖 Automation Scripts
│   ├── playwright_custom_actions.py
│   ├── browser_use_openai_integration.py
│   ├── cdp_integration_examples.py
│   └── multi_agent_parallel_execution.py
└── 🐳 Docker Configuration
    ├── Dockerfile
    ├── docker-compose.yml
    └── requirements.txt
\`\`\`

## 📋 Prerequisites

- **Node.js 18+** 
- **Python 3.8+**
- **Docker & Docker Compose**
- **Google AI Studio API Key** (Gemini)
- **OpenAI API Key** (for automation)

## 🛠️ Quick Start

### 1. Clone the Repository
\`\`\`bash
git clone https://github.com/likhoncodes/ai-medusa.git
cd ai-medusa
\`\`\`

### 2. Environment Setup
\`\`\`bash
# Copy environment template
cp .env.example .env.local

# Add your API keys
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
\`\`\`

### 3. Install Dependencies
\`\`\`bash
# Frontend dependencies
npm install

# Python dependencies for automation
pip install -r requirements.txt
playwright install chromium
\`\`\`

### 4. Start Development
\`\`\`bash
# Start Next.js frontend
npm run dev

# Start FastAPI backend (in another terminal)
cd scripts/backend
python main.py

# Run automation scripts
python scripts/playwright_custom_actions.py
\`\`\`

### 5. Docker Deployment
\`\`\`bash
# Build and run with Docker Compose
docker-compose up --build

# Or build individual containers
npm run docker:build
npm run docker:run
\`\`\`

## 🔧 API Endpoints

### Core System APIs

#### Health Check
\`\`\`http
GET /api/health
\`\`\`

#### Multi-Agent Task Execution
\`\`\`http
POST /api/agents/execute
Content-Type: application/json

{
  "tasks": [
    {
      "type": "web_scraping",
      "url": "https://example.com",
      "selectors": ["h1", ".content"]
    }
  ],
  "agents": 3,
  "priority": "HIGH"
}
\`\`\`

#### Browser Automation
\`\`\`http
POST /api/browser/automate
Content-Type: application/json

{
  "action": "fill_form",
  "url": "https://example.com/form",
  "fields": {
    "email": "user@example.com",
    "password": "secure123"
  }
}
\`\`\`

#### AI Text Generation
\`\`\`http
POST /api/gemini/generate
Content-Type: application/json

{
  "prompt": "Analyze this data and provide insights",
  "data": {...},
  "options": {
    "temperature": 0.7,
    "maxOutputTokens": 1000
  }
}
\`\`\`

### FastAPI Backend APIs

#### Chat System
\`\`\`http
POST /api/v1/chat/sessions
GET /api/v1/chat/sessions/{session_id}/messages
POST /api/v1/chat/sessions/{session_id}/messages
\`\`\`

#### Sandbox Execution
\`\`\`http
POST /api/v1/sandbox/execute
Content-Type: application/json

{
  "command": "python script.py",
  "environment": "python3.8",
  "timeout": 30
}
\`\`\`

## 🤖 Multi-Agent System

### Agent Types
- **WebScraper**: Data extraction, screenshots, content analysis
- **FormFiller**: Form completion, authentication, validation  
- **Tester**: Performance testing, validation, monitoring
- **Monitor**: Health checks, system monitoring, reporting
- **GeneralPurpose**: Flexible automation for various tasks

### Task Priorities
- **CRITICAL**: Maximum retry attempts, immediate execution
- **HIGH**: Standard retry logic, priority queue
- **NORMAL**: Regular processing, balanced resources
- **LOW**: Background processing, minimal retries

### Execution Features
- Parallel task processing across multiple agents
- Intelligent load balancing based on agent capabilities
- Real-time monitoring and performance tracking
- Fault tolerance with automatic error recovery

## 🌐 Browser Automation Capabilities

### Playwright Integration
- **Smart Form Filling**: Multi-strategy field detection and completion
- **Advanced Screenshots**: Full-page, element-specific, masked capture
- **Network Monitoring**: Request tracking and performance analysis
- **Content Extraction**: Structured data extraction with CSS selectors

### Chrome DevTools Protocol (CDP)
- **Performance Monitoring**: Core Web Vitals tracking (LCP, CLS, FID)
- **Memory Analysis**: Heap usage monitoring and leak detection
- **Network Analysis**: Request/response tracking with timing data
- **JavaScript Debugging**: Breakpoint management and exception handling

### AI-Guided Automation
- **Intelligent Decision Making**: OpenAI-powered action planning
- **Adaptive Workflows**: Dynamic task execution based on page analysis
- **Context Awareness**: Smart element detection and interaction
- **Error Recovery**: Automatic retry and alternative action strategies

## 🔒 Security & Isolation

### Docker Sandbox
- Isolated execution environments for each task
- Resource limits and security constraints
- Network isolation and access controls
- Automatic cleanup and container management

### API Security
- JWT authentication for sensitive endpoints
- Rate limiting and request validation
- CORS configuration for cross-origin requests
- Environment variable protection

## 📊 Monitoring & Analytics

### Real-Time Metrics
- Agent performance and utilization
- Task completion rates and timing
- System resource usage
- Error rates and recovery statistics

### Logging System
- Structured JSON logging with context
- Centralized log aggregation
- Error tracking with stack traces
- Performance metrics and profiling

## 🚀 Deployment Options

### Production Deployment
\`\`\`bash
# Docker Compose (Recommended)
docker-compose -f docker-compose.prod.yml up -d

# Kubernetes
kubectl apply -f k8s/

# Vercel (Frontend only)
vercel deploy
\`\`\`

### Environment Configuration
\`\`\`bash
# Production environment variables
GEMINI_API_KEY=prod_gemini_key
OPENAI_API_KEY=prod_openai_key
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379
DOCKER_HOST=unix:///var/run/docker.sock
\`\`\`

## 🧪 Testing

### Automated Testing
\`\`\`bash
# Frontend tests
npm run test

# Backend tests  
cd backend && python -m pytest

# Integration tests
npm run test:integration

# Automation script tests
python -m pytest scripts/tests/
\`\`\`

### Manual Testing
- Interactive API documentation at `/docs`
- Health check endpoints for system validation
- Browser automation test suites
- Multi-agent execution scenarios

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Commit your changes: `git commit -m 'Add amazing feature'`
5. Push to the branch: `git push origin feature/amazing-feature`
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for powerful language processing
- Playwright team for excellent browser automation
- FastAPI for high-performance API framework
- Next.js team for the amazing React framework

## 📞 Support & Community

- 🐛 **Issues**: [GitHub Issues](https://github.com/likhoncodes/ai-medusa/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/likhoncodes/ai-medusa/discussions)
- 📧 **Contact**: [likhoncodes](https://github.com/likhoncodes)

---

<div align="center">
  <strong>Built with ❤️ by <a href="https://github.com/likhoncodes">likhoncodes</a></strong>
</div>
