#!python
"""
BeeAI Python Demo with Observability
This script demonstrates how to use BeeAI with OpenTelemetry instrumentation
and Gemini Flash 1.5 for observability and monitoring.
Integrated with Splunk SignalFX OTEL for production use.
"""

import os
import asyncio
import logging
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenTelemetry imports for Phoenix integration
try:
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.resources import Resource
    OTEL_AVAILABLE = True
    print("✅ OpenTelemetry available for Phoenix integration")
except ImportError:
    OTEL_AVAILABLE = False
    print("⚠️  OpenTelemetry not available. Install with: pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp-proto-http")

# Local implementation of missing BeeAI classes
class LoggerLevel:
    """Logging levels for the BeeAI Logger."""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

class Logger:
    """Simple logger wrapper for BeeAI agents."""
    
    def __init__(self, level=LoggerLevel.INFO):
        self.logger = logging.getLogger("beeai")
        self.logger.setLevel(level)
        
        # Add console handler if none exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def debug(self, message):
        self.logger.debug(message)
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def critical(self, message):
        self.logger.critical(message)

class ChatModel:
    """Simple chat model representation for BeeAI."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

class BaseAgent:
    """Base class for BeeAI agents."""
    
    def __init__(self, name: str, description: str, instructions: str):
        self.name = name
        self.description = description
        self.instructions = instructions

# OpenTelemetry instrumentation for BeeAI
try:
    from openinference.instrumentation.beeai import BeeAIInstrumentor
    OBSERVABILITY_ENABLED = True
    print("✅ OpenTelemetry instrumentation available")
except ImportError:
    OBSERVABILITY_ENABLED = False
    print("⚠️  OpenTelemetry instrumentation not available. Install with: pip install openinference-instrumentation-beeai")

class GeminiFlashAgent(BaseAgent):
    """A BeeAI agent that uses Gemini Flash 1.5 with observability."""
    
    def __init__(self):
        super().__init__(
            name="GeminiFlashAgent",
            description="An AI agent powered by Gemini Flash 1.5 with full observability",
            instructions="""You are a helpful AI assistant powered by Gemini Flash 1.5. 
            Your role is to help users with questions, provide information, and engage in 
            meaningful conversations. Always be helpful, accurate, and friendly."""
        )
        
        # Set up logging
        self.logger = Logger(LoggerLevel.INFO)
        
        # Initialize the chat model (this would connect to Gemini Flash 1.5)
        self.chat_model = ChatModel(
            name="gemini-flash-1.5",
            description="Google's Gemini Flash 1.5 model for fast, efficient AI responses"
        )
        
        # Track conversation history for observability
        self.conversation_history = []
        self.request_count = 0
        
        # Initialize tracer for this agent
        if OTEL_AVAILABLE:
            self.tracer = trace.get_tracer("beeai-gemini-agent")
        else:
            self.tracer = None
        
    async def process_message(self, message: str, context: Dict[str, Any] = None) -> str:
        """Process a user message with full observability."""
        
        # Increment request counter
        self.request_count += 1
        
        # Log the incoming message
        self.logger.info(f"Processing message #{self.request_count}: {message[:50]}...")
        
        # Add to conversation history
        self.conversation_history.append({
            "request_id": self.request_count,
            "user_message": message,
            "timestamp": asyncio.get_event_loop().time(),
            "context": context or {}
        })
        
        # Start OTEL span for message processing
        if self.tracer:
            with self.tracer.start_as_current_span("process_message") as span:
                span.set_attribute("service.name", "beeai-gemini-agent")
                span.set_attribute("agent.name", self.name)
                span.set_attribute("request.id", self.request_count)
                span.set_attribute("llm.prompt", message)
                span.set_attribute("llm.model", "gemini-flash-1.5")
                
                try:
                    # Simulate processing with Gemini Flash 1.5
                    # In a real implementation, this would call the actual Gemini API
                    response = await self._generate_response(message, context)
                    
                    # Log successful response
                    self.logger.info(f"Generated response for request #{self.request_count}")
                    
                    # Update conversation history with response
                    self.conversation_history[-1]["agent_response"] = response
                    self.conversation_history[-1]["status"] = "success"
                    
                    # Set span attributes for successful response
                    span.set_attribute("llm.response", response)
                    span.set_attribute("llm.status", "success")
                    span.set_attribute("llm.response_length", len(response))
                    
                    return response
                    
                except Exception as e:
                    # Log error for observability
                    self.logger.error(f"Error processing request #{self.request_count}: {str(e)}")
                    
                    # Update conversation history with error
                    self.conversation_history[-1]["status"] = "error"
                    self.conversation_history[-1]["error"] = str(e)
                    
                    # Set span attributes for error
                    span.set_attribute("llm.status", "error")
                    span.set_attribute("error.message", str(e))
                    span.set_attribute("error.type", type(e).__name__)
                    
                    # Return fallback response
                    return f"I apologize, but I encountered an error: {str(e)}"
        else:
            # Fallback without OTEL
            try:
                response = await self._generate_response(message, context)
                self.logger.info(f"Generated response for request #{self.request_count}")
                self.conversation_history[-1]["agent_response"] = response
                self.conversation_history[-1]["status"] = "success"
                return response
            except Exception as e:
                self.logger.error(f"Error processing request #{self.request_count}: {str(e)}")
                self.conversation_history[-1]["status"] = "error"
                self.conversation_history[-1]["error"] = str(e)
                return f"I apologize, but I encountered an error: {str(e)}"
    
    async def _generate_response(self, message: str, context: Dict[str, Any] = None) -> str:
        """Generate a response using Gemini Flash 1.5 (simulated)."""
        
        # Simulate API call delay
        await asyncio.sleep(0.1)
        
        # Simple response logic (replace with actual Gemini API call)
        if "hello" in message.lower():
            return "Hello! I'm your Gemini Flash 1.5 powered AI assistant. How can I help you today?"
        elif "help" in message.lower():
            return "I'm here to help! I can answer questions, provide information, and engage in conversations. What would you like to know?"
        elif "beeai" in message.lower():
            return "BeeAI is a powerful framework for building AI agents with built-in observability. It supports OpenTelemetry for monitoring and debugging."
        elif "observability" in message.lower():
            return "Observability in BeeAI includes logging, telemetry collection, and integration with tools like Splunk SignalFX for trace visualization."
        else:
            return f"Thanks for your message: '{message}'. I'm processing this with Gemini Flash 1.5. How can I assist you further?"
    
    def get_observability_data(self) -> Dict[str, Any]:
        """Get observability data for monitoring."""
        return {
            "agent_name": self.name,
            "total_requests": self.request_count,
            "conversation_count": len(self.conversation_history),
            "recent_conversations": self.conversation_history[-5:] if self.conversation_history else [],
            "status": "active"
        }

def setup_splunk_otel():
    """Set up OpenTelemetry for Splunk SignalFX."""
    if not OTEL_AVAILABLE:
        print("⚠️  OpenTelemetry not available - skipping OTEL setup")
        return None
    
    try:
        # Configuration - REPLACE THESE VALUES with your production settings
        OTEL_ENDPOINT = os.getenv("OTEL_ENDPOINT", "http://localhost:4328")  # Your Splunk SignalFX OTEL endpoint
        SERVICE_NAME = os.getenv("SERVICE_NAME", "beeai-gemini-demo")
        ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
        
        print(f"🔧 Setting up Splunk SignalFX OTEL integration...")
        print(f"   Endpoint: {OTEL_ENDPOINT}")
        print(f"   Service: {SERVICE_NAME}")
        print(f"   Environment: {ENVIRONMENT}")
        
        # Create resource with service information
        resource = Resource.create({
            "service.name": SERVICE_NAME,
            "service.version": "1.0.0",
            "deployment.environment": ENVIRONMENT,
            "telemetry.sdk.name": "beeai-framework",
            "telemetry.sdk.version": "0.1.17"
        })
        
        # Create tracer provider
        tracer_provider = TracerProvider(resource=resource)
        
        # Create OTLP exporter for Splunk SignalFX
        otlp_exporter = OTLPSpanExporter(
            endpoint=OTEL_ENDPOINT,
            headers={
                # Add any required headers for your Splunk setup
                # "Authorization": "Bearer your-token",
                # "X-SF-TOKEN": "your-signalfx-token"
            }
        )
        
        # Add batch processor
        tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
        
        # Set as global tracer provider
        trace.set_tracer_provider(tracer_provider)
        
        print("✅ Splunk SignalFX OTEL integration configured successfully")
        return tracer_provider
        
    except Exception as e:
        print(f"⚠️  Failed to configure Splunk SignalFX OTEL: {e}")
        print("💡 Check your OTEL endpoint and configuration")
        return None

def setup_phoenix_otel(endpoint: str, project_name: str):
    """Set up OpenTelemetry integration for Phoenix."""
    try:
        print(f"🔧 Setting up Phoenix OTEL integration...")
        print(f"   Endpoint: {endpoint}")
        print(f"   Project: {project_name}")
        
        # Create resource with project information
        resource = Resource.create({
            "service.name": project_name,
            "service.version": "1.0.0",
            "deployment.environment": "development",
            "telemetry.sdk.name": "beeai-framework",
            "telemetry.sdk.version": "0.1.17"
        })
        
        # Create tracer provider
        tracer_provider = TracerProvider(resource=resource)
        
        # Create OTLP exporter for Phoenix
        otlp_exporter = OTLPSpanExporter(
            endpoint=f"{endpoint}/v1/traces",
            headers={
                # Phoenix typically doesn't require special headers
            }
        )
        
        # Add batch processor
        tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
        
        # Set as global tracer provider
        trace.set_tracer_provider(tracer_provider)
        
        print("✅ Phoenix OTEL integration configured successfully")
        return tracer_provider
        
    except Exception as e:
        print(f"⚠️  Failed to configure Phoenix OTEL: {e}")
        print("💡 Check your Phoenix endpoint and configuration")
        return None

async def main():
    """Main function to demonstrate BeeAI with observability."""
    
    print("🐝 Welcome to BeeAI Python Demo with Observability!")
    print("🚀 Using Gemini Flash 1.5 with Phoenix OpenTelemetry")
    
    # Set up OpenTelemetry integration for Phoenix
    tracer_provider = None
    if OTEL_AVAILABLE:
        try:
            # Get Phoenix configuration from environment variables
            phoenix_endpoint = os.getenv("PHOENIX_COLLECTOR_ENDPOINT", "http://localhost:6006")
            phoenix_project = os.getenv("PHOENIX_PROJECT_NAME", "beeai-demo")
            
            # Configure OpenTelemetry to send traces to Phoenix
            tracer_provider = setup_phoenix_otel(phoenix_endpoint, phoenix_project)
            if tracer_provider:
                print("✅ OpenTelemetry configured for Phoenix successfully")
                print(f"   Project: {phoenix_project}")
                print(f"   Endpoint: {phoenix_endpoint}/v1/traces")
        except Exception as e:
            print(f"⚠️  Failed to configure OpenTelemetry for Phoenix: {e}")
            print("💡 Make sure Phoenix is running on port 6006")
            # Fallback to Splunk configuration
            tracer_provider = setup_splunk_otel()
    
    # Enable OpenTelemetry instrumentation if available
    if OBSERVABILITY_ENABLED and tracer_provider:
        try:
            BeeAIInstrumentor().instrument()
            print("✅ OpenTelemetry instrumentation enabled")
        except Exception as e:
            print(f"⚠️  Failed to enable instrumentation: {e}")
    
    # Check for required environment variables
    api_key = os.getenv("BEEAI_API_KEY")
    if not api_key:
        print("⚠️  BEEAI_API_KEY not found in environment variables")
        print("💡 Create a .env file with your API key to enable full functionality")
    
    # Create the agent
    agent = GeminiFlashAgent()
    print(f"✅ Agent created: {agent.name}")
    
    # Demonstrate the agent with some test messages
    test_messages = [
        "Hello! How are you today?",
        "Can you tell me about BeeAI?",
        "What is observability?",
        "How does Gemini Flash 1.5 work?",
        "Can you help me with a coding problem?"
    ]
    
    print("\n🤖 Testing the agent with sample messages:")
    print("=" * 50)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 Test {i}: {message}")
        response = await agent.process_message(message)
        print(f"🤖 Response: {response}")
        
        # Small delay between requests
        await asyncio.sleep(0.5)
    
    # Show observability data
    print("\n📊 Observability Data:")
    print("=" * 50)
    obs_data = agent.get_observability_data()
    for key, value in obs_data.items():
        if key != "recent_conversations":
            print(f"  {key}: {value}")
    
    print(f"\n  recent_conversations: {len(obs_data['recent_conversations'])} items")
    
    print("\n🎉 Demo completed successfully!")
    
    if tracer_provider:
        phoenix_endpoint = os.getenv("PHOENIX_COLLECTOR_ENDPOINT", "http://localhost:6006")
        phoenix_project = os.getenv("PHOENIX_PROJECT_NAME", "beeai-demo")
        if "phoenix" in phoenix_endpoint.lower() or "6006" in phoenix_endpoint:
            print("💡 Check your traces in Phoenix Dashboard")
            print(f"   Project: {phoenix_project}")
            print(f"   URL: {phoenix_endpoint}")
        else:
            print("💡 Check your traces in Splunk SignalFX")
            print("   Service: beeai-gemini-demo")
        print("   Environment: development")
    else:
        print("💡 Install OpenTelemetry for trace collection: pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp-proto-http")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
