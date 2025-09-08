# Gemini Backend System

A comprehensive, scalable backend system powered by Google's Gemini AI model, featuring advanced data processing capabilities, robust error handling, and seamless API integration.

## 🚀 Features

- **Gemini AI Integration**: Leverage Google's advanced Gemini model for intelligent text generation and data analysis
- **Data Processing**: Advanced data transformation, normalization, aggregation, and validation
- **API Integration**: RESTful APIs for seamless front-end communication
- **Error Handling**: Robust error handling with structured logging and validation
- **Scalable Architecture**: Modular design for easy maintenance and future enhancements
- **TypeScript**: Full type safety and enhanced developer experience
- **Browser Automation System**: Comprehensive Python-based browser automation with advanced integration examples

## 📋 Prerequisites

- Node.js 18+ 
- Google AI Studio API Key (Gemini)
- Next.js 15+
- Python 3.8+
- Playwright
- OpenAI API Key (for automation scripts)

## 🛠️ Installation

1. **Clone and install dependencies:**
   \`\`\`bash
   npm install
   \`\`\`

2. **Set up environment variables:**
   \`\`\`bash
   # Create .env.local file
   GEMINI_API_KEY=your_gemini_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   \`\`\`

3. **Get your Gemini API Key:**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add it to your environment variables

4. **Get your OpenAI API Key:**
   - Visit [OpenAI](https://openai.com/)
   - Create a new API key
   - Add it to your environment variables

5. **Install Python dependencies for browser automation:**
   \`\`\`bash
   pip install playwright asyncio logging dataclasses
   playwright install chromium
   \`\`\`

6. **Start the development server:**
   \`\`\`bash
   npm run dev
   \`\`\`

## 🔧 API Endpoints

### Health Check
\`\`\`http
GET /api/health
\`\`\`
Returns system health status and service information.

### Text Generation
\`\`\`http
POST /api/gemini/generate
Content-Type: application/json

{
  "prompt": "Explain quantum computing in simple terms",
  "options": {
    "temperature": 0.7,
    "maxOutputTokens": 500
  }
}
\`\`\`

### Data Processing
\`\`\`http
POST /api/data/process
Content-Type: application/json

{
  "data": [{"name": "John", "age": 30}],
  "operation": "transform",
  "options": {
    "transformationType": "normalize"
  }
}
\`\`\`

**Available Operations:**
- `transform`: Data transformation (normalize, aggregate, filter, enrich)
- `analyze`: AI-powered analysis (summary, sentiment, classification, extraction)
- `validate`: Data validation and quality checks
- `process`: Custom data processing with AI instructions

### API Documentation
\`\`\`http
GET /api/docs
\`\`\`
Returns complete API documentation with examples.

## 🏗️ Architecture

### Core Services

- **GeminiService** (`lib/gemini.ts`): Handles all Gemini AI interactions
- **DataProcessor** (`lib/data-processor.ts`): Advanced data processing operations
- **ErrorHandler** (`lib/error-handler.ts`): Centralized error handling and validation

### API Routes

- `/api/health`: System health monitoring
- `/api/gemini/generate`: Text generation endpoint
- `/api/data/process`: Data processing endpoint
- `/api/docs`: API documentation

### Browser Automation Components

#### 1. Playwright Custom Actions (`scripts/playwright_custom_actions.py`)
- **Smart Form Filling**: Intelligent field detection and multi-strategy form completion
- **Advanced Screenshots**: Full-page, element-specific, and masked screenshot capture
- **Structured Text Extraction**: Configurable content extraction with CSS selectors
- **Network Monitoring**: Wait for network idle and track page load performance

**Key Features:**
- Multiple field detection strategies (name, id, placeholder, label association)
- Screenshot masking for sensitive data
- Comprehensive error handling and logging
- Realistic browser configuration to avoid detection

#### 2. Browser-Use with OpenAI Integration (`scripts/browser_use_openai_integration.py`)
- **AI-Guided Automation**: Use OpenAI models for intelligent decision-making
- **Adaptive Workflows**: Dynamic action planning based on page analysis
- **Multi-Step Task Execution**: Coordinate complex browser workflows
- **Task History Tracking**: Comprehensive execution reporting and analysis

**Key Features:**
- AI-powered page analysis and action recommendation
- Intelligent task coordination and workflow management
- Comprehensive task history and performance reporting
- Error recovery and continuation logic

#### 3. Chrome DevTools Protocol (CDP) Integration (`scripts/cdp_integration_examples.py`)
- **Performance Monitoring**: Real-time performance metrics and optimization recommendations
- **Network Analysis**: Request/response tracking and failure detection
- **Memory Monitoring**: JavaScript heap usage and memory leak detection
- **JavaScript Debugging**: Breakpoint management and exception handling

**Key Features:**
- Core Web Vitals monitoring (LCP, CLS, FID)
- Network request analysis with timing and failure tracking
- Memory usage monitoring with leak detection
- Advanced debugging capabilities with breakpoint management

#### 4. Multi-Agent Parallel Execution (`scripts/multi_agent_parallel_execution.py`)
- **Parallel Processing**: Multiple browser agents working simultaneously
- **Intelligent Load Balancing**: Task distribution based on agent capabilities
- **Fault Tolerance**: Error recovery and agent health monitoring
- **Real-Time Monitoring**: Live performance tracking and reporting

**Key Features:**
- Agent capability matching for optimal task assignment
- Priority-based task queue management
- Comprehensive agent health monitoring and recovery
- Real-time performance metrics and reporting

## 🔒 Error Handling

The system includes comprehensive error handling:

- **Custom Error Classes**: APIError, ValidationError, GeminiError, DataProcessingError
- **Structured Logging**: JSON-formatted logs with context
- **Validation**: Request validation with detailed error messages
- **Environment Checks**: Automatic validation of required environment variables

## 📊 Data Processing Capabilities

### Transformation Types
- **Normalize**: Clean and standardize data formats
- **Aggregate**: Summarize and calculate statistics
- **Filter**: Remove irrelevant or low-quality data
- **Enrich**: Add context and insights using AI

### Analysis Types
- **Summary**: Generate comprehensive summaries
- **Sentiment**: Analyze emotional tone and sentiment
- **Classification**: Categorize and organize data
- **Extraction**: Extract key entities and information

## 🚀 Deployment

### Vercel (Recommended)
\`\`\`bash
npm run build
# Deploy to Vercel with environment variables set
\`\`\`

### Docker
\`\`\`dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
\`\`\`

## 🔧 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `NEXT_PUBLIC_API_URL`: Base URL for API endpoints (optional)
- `OPENAI_API_KEY`: Your OpenAI API key (required for automation scripts)

### Gemini Model Configuration
Default model: `gemini-1.5-flash`
- Configurable in `lib/gemini.ts`
- Supports all Gemini model variants

### Automation Configuration

#### Agent Capabilities
- **WebScraper**: Data extraction, screenshots, content analysis
- **FormFiller**: Form completion, authentication, validation
- **Tester**: Performance testing, validation, monitoring
- **Monitor**: Health checks, system monitoring, reporting
- **GeneralPurpose**: Flexible automation for various tasks

#### Task Priorities
- **CRITICAL**: High-priority tasks with maximum retry attempts
- **HIGH**: Important tasks with standard retry logic
- **NORMAL**: Regular tasks with basic error handling
- **LOW**: Background tasks with minimal retry attempts

## 📈 Monitoring and Logging

- Health check endpoint for monitoring
- Structured JSON logging
- Error tracking with context
- Performance metrics available

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the API documentation at `/api/docs`
2. Review the health status at `/api/health`
3. Check environment variable configuration
4. Verify Gemini API key is valid
5. Review automation script documentation and execution reports

## 🔄 Version History

- **v1.0.0**: Initial release with core functionality
  - Gemini AI integration
  - Data processing capabilities
  - Error handling system
  - API endpoints
  - Documentation
  - Browser automation system
