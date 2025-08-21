# 🚀 Quick Start Guide - BeeAI Python Demo

## 📋 What You'll Get

✅ **BeeAI Python Agent** with Gemini Flash 1.5 simulation  
✅ **Full Observability** with OpenTelemetry instrumentation  
✅ **Phoenix Integration** for trace visualization  
✅ **Comprehensive Logging** and monitoring  

## ⚡ 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your BeeAI API key
# Get it from: https://beeai.com
```

### 3. Start Phoenix (Optional but Recommended)
```bash
# Option A: Using BeeAI CLI (if you have it)
beeai platform start --set phoenix.enabled=true

# Option B: Install Phoenix separately
pip install phoenix
phoenix start
```

### 4. Test Phoenix Connection
```bash
python test_phoenix_integration.py
```

### 5. Run the Demo
```bash
python beeai_python_demo.py
```

## 🔍 What You'll See

### Terminal Output
- Agent creation and configuration
- Sample conversations with Gemini Flash 1.5
- Observability data and metrics
- Phoenix integration status

### Phoenix Dashboard (http://localhost:6006)
- **Project**: beeai-demo
- **Real-time traces** of agent operations
- **Performance metrics** and timing
- **Error tracking** and debugging info

## 🎯 Key Features Demonstrated

1. **Agent Creation** - Custom Gemini Flash 1.5 agent
2. **Message Processing** - Async conversation handling
3. **Observability** - Comprehensive logging and tracing
4. **Phoenix Integration** - Real-time trace visualization
5. **Error Handling** - Graceful fallbacks and logging

## 🚨 Troubleshooting

### Phoenix Not Starting?
```bash
# Check if port 6006 is available
netstat -an | findstr 6006

# Try different port
phoenix start --port 6007
```

### Import Errors?
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### API Key Issues?
- Verify .env file exists
- Check API key format
- Ensure BeeAI service is accessible

## 🔗 Useful URLs

- **Phoenix Dashboard**: http://localhost:6006
- **Trace Endpoint**: http://localhost:6006/v1/traces
- **BeeAI Docs**: https://docs.beeai.dev
- **Phoenix Docs**: https://docs.beeai.dev/how-to/observe-agents

## 🎉 Success Indicators

✅ Phoenix accessible at http://localhost:6006  
✅ Demo runs without errors  
✅ Traces appear in Phoenix dashboard  
✅ Observability data shows in terminal  

## 🚀 Next Steps

1. **Real Gemini Integration** - Replace simulated responses
2. **Custom Metrics** - Add business-specific monitoring
3. **Production Deployment** - Scale and optimize
4. **Custom Dashboards** - Build Phoenix visualizations

---

**Need Help?** Check the full [PYTHON_README.md](PYTHON_README.md) for detailed documentation.
