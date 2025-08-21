# 🚀 Quick Start Guide - BeeAI with Splunk SignalFX

## 📋 What You'll Get

✅ **BeeAI Python Agent** with Gemini Flash 1.5 simulation  
✅ **Splunk SignalFX OTEL Integration** for production observability  
✅ **Custom LLM Tracing** with rich span attributes  
✅ **Production-ready configuration**  

## ⚡ 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Production Environment
```bash
# Copy production environment template
cp .env.production .env

# Edit .env with your actual values
OTEL_ENDPOINT=http://your-splunk-signalfx-endpoint:port
SERVICE_NAME=your-service-name
ENVIRONMENT=production
BEEAI_API_KEY=your-actual-api-key
```

### 3. Test OTEL Connection
```bash
# Test if your OTEL endpoint is accessible
curl http://your-splunk-signalfx-endpoint:port/health
```

### 4. Run the Demo
```bash
python beeai_python_demo.py
```

## 🔍 What You'll See

### Terminal Output
- Agent creation and configuration
- Sample conversations with Gemini Flash 1.5
- **Splunk SignalFX OTEL setup confirmation**
- Observability data and metrics

### Splunk SignalFX Dashboard
- **Service**: Your configured service name
- **Real-time traces** of agent operations
- **LLM-specific attributes** (prompts, responses, models)
- **Performance metrics** and error tracking

## 🎯 Key Features for Production

1. **Direct OTEL Export** - No Phoenix dependency
2. **Rich Span Attributes** - LLM-specific metadata
3. **Batch Processing** - Efficient trace collection
4. **Environment Configuration** - Development/Production separation
5. **Error Handling** - Graceful fallbacks and logging

## 🔧 Production Configuration

### Environment Variables
```bash
# Required
OTEL_ENDPOINT=http://your-splunk-signalfx-endpoint:port
SERVICE_NAME=your-service-name
ENVIRONMENT=production
BEEAI_API_KEY=your-api-key

# Optional
OTEL_HEADERS_AUTHORIZATION=Bearer your-token
OTEL_HEADERS_X_SF_TOKEN=your-signalfx-token
```

### Custom Headers
If your Splunk setup requires authentication:
```python
# In .env
OTEL_HEADERS_AUTHORIZATION=Bearer your-token
OTEL_HEADERS_X_SF_TOKEN=your-signalfx-token

# The demo will automatically include these in OTLP requests
```

## 🚨 Troubleshooting

### OTEL Connection Issues
```bash
# Check endpoint accessibility
curl -v http://your-endpoint:port

# Check network connectivity
telnet your-endpoint port

# Verify Docker container is running
docker ps | grep splunk-signalfx
```

### Import Errors
```bash
# Reinstall OpenTelemetry packages
pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp-proto-http --force-reinstall
```

### Authentication Issues
- Verify token format (Bearer prefix for Authorization)
- Check token permissions in Splunk
- Verify IP whitelist if configured

## 🔗 Useful Commands

### Test OTEL Export
```bash
# Test with simple Python script
python -c "
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

provider = TracerProvider()
exporter = OTLPSpanExporter(endpoint='http://your-endpoint:port')
provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer('test')
with tracer.start_as_current_span('test_span') as span:
    span.set_attribute('test.attribute', 'test_value')
    print('Test span created and exported')
"
```

### Check Environment
```bash
# Verify environment variables
python -c "import os; print('OTEL_ENDPOINT:', os.getenv('OTEL_ENDPOINT')); print('SERVICE_NAME:', os.getenv('SERVICE_NAME'))"
```

## 🌐 Splunk SignalFX Integration

### Trace Flow
1. **BeeAI Agent** processes message
2. **OpenTelemetry** creates span with LLM attributes
3. **OTLP Exporter** sends to your Splunk endpoint
4. **Splunk SignalFX** processes and displays traces
5. **Splunk** provides visualization and alerting

### Span Attributes
Each trace includes:
- `service.name`: Your service identifier
- `llm.prompt`: User input message
- `llm.response`: AI response content
- `llm.model`: Model identifier (gemini-flash-1.5)
- `llm.status`: Success/error status
- `request.id`: Unique request identifier

## 🎉 Success Indicators

✅ OTEL endpoint accessible  
✅ Demo runs without errors  
✅ Traces appear in Splunk dashboard  
✅ Rich LLM attributes visible  
✅ Service name correctly identified  

## 🚀 Next Steps

1. **Real Gemini Integration** - Replace simulated responses
2. **Custom Attributes** - Add business-specific metadata
3. **Alerting** - Configure Splunk alerts for errors
4. **Dashboards** - Build custom Splunk visualizations
5. **Metrics** - Add custom metrics collection

---

**Need Help?** Check the full [PYTHON_README.md](PYTHON_README.md) for detailed documentation.
