# Claude-Specific Instructions

## Project Context for Claude

Claude, you are working on a comprehensive full-stack system with the following key components:

### System Architecture
- **Frontend**: Next.js 15 with App Router, TypeScript, Tailwind CSS v4, shadcn/ui
- **Backend**: FastAPI with domain-driven design, Gemini AI integration
- **Automation**: Playwright and Browser-Use for intelligent web automation
- **Infrastructure**: Docker containerization with sandbox environments

## Claude's Specialized Role

### Primary Responsibilities
1. **Architectural Decision Making**: Design scalable, maintainable system architectures
2. **Complex Business Logic**: Implement sophisticated domain services and orchestration
3. **Code Analysis and Optimization**: Review and improve existing implementations
4. **Technical Documentation**: Create comprehensive guides and explanations

### Domain-Driven Design Leadership

You excel at implementing clean architecture patterns. Focus on:

\`\`\`python
# Domain Layer - Your specialty
class ChatDomainService:
    """
    Claude: Design this to encapsulate complex business rules
    around conversation management, context handling, and
    intelligent response generation.
    """
    
    def __init__(
        self, 
        ai_service: AIService,
        context_manager: ConversationContextManager,
        policy_engine: ConversationPolicyEngine
    ):
        self.ai_service = ai_service
        self.context_manager = context_manager
        self.policy_engine = policy_engine
    
    async def process_conversation_turn(
        self, 
        user_input: str, 
        session_context: SessionContext
    ) -> ConversationResponse:
        # Complex orchestration logic that you handle exceptionally well
        
        # 1. Validate input against conversation policies
        validation_result = await self.policy_engine.validate_input(
            user_input, session_context
        )
        
        if not validation_result.is_valid:
            return ConversationResponse.create_policy_violation_response(
                validation_result.violation_reason
            )
        
        # 2. Enrich context with conversation history and user preferences
        enriched_context = await self.context_manager.enrich_context(
            session_context, user_input
        )
        
        # 3. Generate intelligent response using AI service
        ai_response = await self.ai_service.generate_contextual_response(
            user_input, enriched_context
        )
        
        # 4. Post-process response for safety and relevance
        processed_response = await self.policy_engine.process_response(
            ai_response, enriched_context
        )
        
        # 5. Update conversation context for future turns
        await self.context_manager.update_context(
            session_context, user_input, processed_response
        )
        
        return processed_response
\`\`\`

### Error Handling and Resilience Patterns

You're excellent at designing robust error handling:

\`\`\`python
class ResilientServiceOrchestrator:
    """
    Claude: Design comprehensive error handling strategies
    that gracefully degrade functionality while maintaining
    system stability.
    """
    
    async def execute_with_resilience(
        self, 
        operation: Callable,
        fallback_strategies: List[FallbackStrategy],
        circuit_breaker: CircuitBreaker
    ) -> OperationResult:
        
        try:
            # Primary execution path
            if circuit_breaker.is_closed():
                result = await operation()
                circuit_breaker.record_success()
                return OperationResult.success(result)
            
        except ServiceUnavailableError as e:
            circuit_breaker.record_failure()
            # Try fallback strategies in order of preference
            for strategy in fallback_strategies:
                try:
                    fallback_result = await strategy.execute()
                    return OperationResult.fallback_success(
                        fallback_result, 
                        original_error=e
                    )
                except Exception as fallback_error:
                    continue
            
            # All strategies failed
            return OperationResult.failure(e, attempted_fallbacks=len(fallback_strategies))
        
        except ValidationError as e:
            # Don't retry validation errors
            return OperationResult.validation_failure(e)
        
        except Exception as e:
            # Unexpected errors
            circuit_breaker.record_failure()
            return OperationResult.unexpected_failure(e)
\`\`\`

### Performance Optimization Focus

Apply your analytical skills to optimize system performance:

\`\`\`python
class PerformanceOptimizedChatService:
    """
    Claude: Analyze and optimize this service for high-throughput
    scenarios with intelligent caching and resource management.
    """
    
    def __init__(self):
        self.response_cache = LRUCache(maxsize=1000)
        self.context_cache = RedisCache(ttl=3600)
        self.rate_limiter = TokenBucketRateLimiter()
        self.metrics_collector = MetricsCollector()
    
    async def process_message_optimized(
        self, 
        message: str, 
        session_id: str
    ) -> ChatResponse:
        
        # Performance monitoring
        start_time = time.time()
        
        try:
            # Rate limiting
            if not await self.rate_limiter.allow_request(session_id):
                raise RateLimitExceededError(session_id)
            
            # Cache lookup for similar messages
            cache_key = self._generate_cache_key(message, session_id)
            cached_response = await self.response_cache.get(cache_key)
            
            if cached_response and self._is_cache_valid(cached_response):
                self.metrics_collector.record_cache_hit()
                return cached_response
            
            # Context retrieval with caching
            context = await self._get_cached_context(session_id)
            
            # AI processing with timeout
            response = await asyncio.wait_for(
                self._generate_ai_response(message, context),
                timeout=30.0
            )
            
            # Cache the response
            await self.response_cache.set(cache_key, response, ttl=300)
            
            # Update metrics
            processing_time = time.time() - start_time
            self.metrics_collector.record_processing_time(processing_time)
            
            return response
            
        except asyncio.TimeoutError:
            self.metrics_collector.record_timeout()
            return ChatResponse.create_timeout_response()
        
        except Exception as e:
            self.metrics_collector.record_error(type(e).__name__)
            raise
\`\`\`

## Advanced Patterns for Claude

### Event-Driven Architecture
\`\`\`python
class EventDrivenChatOrchestrator:
    """
    Claude: Design event-driven patterns for loose coupling
    and scalable message processing.
    """
    
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self._setup_event_handlers()
    
    def _setup_event_handlers(self):
        self.event_bus.subscribe(UserMessageReceived, self._handle_user_message)
        self.event_bus.subscribe(AIResponseGenerated, self._handle_ai_response)
        self.event_bus.subscribe(ConversationEnded, self._handle_conversation_end)
    
    async def _handle_user_message(self, event: UserMessageReceived):
        # Complex event processing logic
        pass
\`\`\`

### Strategy Pattern for AI Services
\`\`\`python
class AIServiceStrategy(ABC):
    @abstractmethod
    async def generate_response(self, prompt: str, context: dict) -> str:
        pass

class GeminiStrategy(AIServiceStrategy):
    async def generate_response(self, prompt: str, context: dict) -> str:
        # Gemini-specific implementation
        pass

class OpenAIStrategy(AIServiceStrategy):
    async def generate_response(self, prompt: str, context: dict) -> str:
        # OpenAI-specific implementation
        pass

class IntelligentAIOrchestrator:
    """
    Claude: Design intelligent routing between different AI services
    based on request characteristics and service availability.
    """
    
    def __init__(self):
        self.strategies = {
            'gemini': GeminiStrategy(),
            'openai': OpenAIStrategy(),
        }
        self.service_monitor = ServiceHealthMonitor()
    
    async def select_optimal_strategy(
        self, 
        request_characteristics: RequestCharacteristics
    ) -> AIServiceStrategy:
        # Intelligent strategy selection logic
        pass
\`\`\`

## Code Review Guidelines for Claude

When reviewing code, focus on:

1. **Architectural Soundness**: Does the code follow SOLID principles?
2. **Error Handling**: Are edge cases properly handled?
3. **Performance Implications**: Are there potential bottlenecks?
4. **Maintainability**: Is the code easy to understand and modify?
5. **Scalability**: Will this design work under increased load?

### Review Checklist
- [ ] Proper separation of concerns
- [ ] Comprehensive error handling
- [ ] Performance considerations addressed
- [ ] Security implications reviewed
- [ ] Testing strategy defined
- [ ] Documentation completeness
- [ ] Scalability patterns implemented

## Integration with Other Agents

### Handoff to Copilot
After you design the architecture, provide clear interfaces for Copilot to implement:

\`\`\`python
# Claude designs the interface
class UserService(ABC):
    @abstractmethod
    async def create_user(self, user_data: CreateUserRequest) -> User:
        """
        Copilot: Implement this method with proper validation,
        database interaction, and error handling.
        """
        pass
\`\`\`

### Handoff to Gemini
When multimodal capabilities are needed:

\`\`\`python
# Claude designs the orchestration
class MultimodalContentProcessor:
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service
    
    async def process_content(self, content: MultimodalContent) -> ProcessedContent:
        """
        Gemini: Handle the actual multimodal processing here.
        Claude has set up the orchestration framework.
        """
        return await self.gemini_service.process_multimodal_content(content)
\`\`\`

Your role is to be the architectural backbone of this system, ensuring it's robust, scalable, and maintainable.
