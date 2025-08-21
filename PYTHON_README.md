# 🐝 BeeAI Python Demo with Observability

This Python demo showcases BeeAI with full observability features, including OpenTelemetry instrumentation, Splunk SignalFX integration, and Gemini Flash 1.5.

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip package manager
- BeeAI API key
- Splunk SignalFX OTEL endpoint accessible

### Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your environment:**
   ```bash
   # For development
   cp .env.example .env
   
   # For production (Splunk SignalFX)
   cp .env.production .env
   
   # Edit .env and add your configuration
   # Get your API key from: https://beeai.com
   ```

3. **Configure Splunk SignalFX OTEL:**
   ```bash
   # Update .env with your OTEL endpoint
   OTEL_ENDPOINT=http://your-splunk-signalfx-endpoint:port
   SERVICE_NAME=your-service-name
   ENVIRONMENT=production
   ```

4. **Run the demo:**
   ```bash
   python beeai_python_demo.py
   ```

## 🔍 Observability Features

This demo includes several observability features integrated with **Splunk SignalFX**:

### 1. Splunk SignalFX OTEL Integration
- **Direct OTLP export** to your Splunk SignalFX endpoint
- **Service-based organization** with proper resource attributes
- **Batch span processing** for efficient trace collection
- **Production-ready configuration** with environment variables

### 2. OpenTelemetry Instrumentation
- Automatic tracing of agent operations
- Performance metrics collection
- Error tracking and debugging
- **Custom span attributes** for LLM operations

### 3. Built-in Logging
- Structured logging with BeeAI Logger
- Request/response tracking
- Error logging with context

### 4. Conversation History
- Track all user interactions
- Monitor agent performance
- Debug conversation flows

## 🎯 What the Demo Does

1. **Creates a Gemini Flash 1.5 Agent**
   - Extends BeeAI's BaseAgent
   - Simulates Gemini Flash 1.5 responses
   - Includes comprehensive error handling

2. **Demonstrates Observability**
   - Logs all operations
   - Tracks conversation history
   - Provides monitoring data
   - **Integrates with Splunk SignalFX for trace visualization**

3. **Tests Agent Functionality**
   - Processes sample messages
   - Shows response generation
   - Demonstrates error handling

## 🔧 Configuration

### Environment Variables
- `BEEAI_API_KEY`: Your BeeAI API key (required for full functionality)
- `OTEL_ENDPOINT`: Your Splunk SignalFX OTEL endpoint (e.g., http://localhost:4328)
- `SERVICE_NAME`: Service name for identification in Splunk
- `ENVIRONMENT`: Deployment environment (development/staging/production)

### Splunk SignalFX Configuration
The demo automatically configures OTEL integration:
```python
# Creates OTLP exporter for your endpoint
otlp_exporter = OTLPSpanExporter(
    endpoint=OTEL_ENDPOINT,
    headers={
        # Add any required headers for your Splunk setup
        # "Authorization": "Bearer your-token",
        # "X-SF-TOKEN": "your-signalfx-token"
    }
)
```

### Agent Configuration
The agent is configured in the `GeminiFlashAgent` class:
- Name: "GeminiFlashAgent"
- Model: Gemini Flash 1.5 (simulated)
- Instructions: Helpful AI assistant behavior

## 📊 Observability Data

The demo provides:
- **Request Count**: Total messages processed
- **Conversation History**: Recent interactions
- **Status Tracking**: Success/error rates
- **Performance Metrics**: Response times
- **Splunk Traces**: Full execution traces in your Splunk dashboard

## 🚀 Next Steps

### Enable Real Gemini Flash 1.5
1. Get a Google AI API key
2. Replace the simulated response logic
3. Add actual Gemini API calls

### Enhanced Observability
1. **Splunk SignalFX is already configured** - view traces in your Splunk dashboard
2. Add custom metrics and attributes
3. Integrate with your existing monitoring systems

### Production Features
1. Add authentication headers for Splunk
2. Implement rate limiting
3. Add persistent storage
4. Configure proper error handling

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **Splunk SignalFX Connection Issues**
   - Check OTEL endpoint is accessible
   - Verify network connectivity
   - Check firewall settings
   - Verify authentication if required

3. **OpenTelemetry Issues**
   - Check OTEL endpoint configuration
   - Verify instrumentation is enabled
   - Check network connectivity

4. **API Key Issues**
   - Verify .env file exists
   - Check API key format
   - Ensure API key is valid

## 🌐 Splunk SignalFX Integration

### Configuration
- **OTEL Endpoint**: Configured via `OTEL_ENDPOINT` environment variable
- **Service Name**: Identifies your service in Splunk
- **Environment**: Tracks deployment environment
- **Resource Attributes**: Includes SDK and version information

### Trace Information
- **Service**: beeai-gemini-agent (configurable)
- **Environment**: development/production (configurable)
- **OTLP Export**: HTTP protocol to your endpoint
- **Batch Processing**: Efficient trace collection

### Custom Attributes
The demo adds rich span attributes:
- `llm.prompt`: User input message
- `llm.response`: AI response content
- `llm.model`: Model identifier
- `llm.status`: Success/error status
- `request.id`: Unique request identifier

## 📚 Learn More

- [BeeAI Observability Documentation](https://docs.beeai.dev/how-to/observe-agents)
- [OpenTelemetry Instrumentation](https://docs.beeai.dev/how-to/observe-agents#instrumenting-with-openinference)
- [Splunk SignalFX Documentation](https://docs.splunk.com/Documentation/SignalFx)
- [OpenTelemetry OTLP Export](https://opentelemetry.io/docs/specs/otlp/)

## 🤝 Contributing

Feel free to enhance this demo with:
- Real Gemini API integration
- Additional observability features
- Performance optimizations
- Error handling improvements
- Custom Splunk dashboards
- Additional OTEL exporters
