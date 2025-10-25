# Single-Session Testing Guide

This document demonstrates how to test the entire ML microservice in a single terminal session, addressing the issue of "making different terminals to run commands."

## Single Command Chain Approach

You can run all testing steps in one command chain:

```bash
cd /home/runner/work/blindhire/blindhire/ml_service && \
pip install -r requirements.txt && \
ML_USE_FALLBACK=true python app.py > /tmp/ml_service.log 2>&1 & \
SERVICE_PID=$! && \
echo "Service started with PID: $SERVICE_PID" && \
sleep 5 && \
echo "=== Health Check ===" && \
curl -s http://127.0.0.1:8001/health | python -m json.tool && \
echo -e "\n=== Quick Test ===" && \
python quick_test.py && \
echo -e "\n=== Comprehensive Tests ===" && \
python tests/test_local.py && \
echo -e "\n=== Stopping Service ===" && \
kill $SERVICE_PID && \
echo "All tests completed in single session!"
```

## Why This Works

1. **Command Chaining with `&&`**: Each command runs only if the previous one succeeds
2. **Background Process with `&`**: Service runs in background while tests execute in foreground
3. **PID Tracking**: We capture the service PID to cleanly stop it later
4. **Single Terminal**: Everything runs in one session, no context switching needed

## Step-by-Step Breakdown

If you prefer to see each step:

```bash
# 1. Install dependencies (one time)
cd /home/runner/work/blindhire/blindhire/ml_service
pip install -r requirements.txt

# 2. Start service in background
ML_USE_FALLBACK=true python app.py &
SERVICE_PID=$!

# 3. Wait for startup
sleep 5

# 4. Test health endpoint
curl http://127.0.0.1:8001/health

# 5. Run tests
python quick_test.py
python tests/test_local.py

# 6. Stop service
kill $SERVICE_PID
```

## Production Usage

For production (with full transformer model):

```bash
# Single command - downloads model on first run
cd /home/runner/work/blindhire/blindhire/ml_service && \
pip install -r requirements.txt && \
python app.py
```

Or with explicit environment variable:

```bash
cd /home/runner/work/blindhire/blindhire/ml_service && \
ML_USE_FALLBACK=false python app.py
```

## Key Benefits

✅ **Single session**: No need to switch between multiple terminals  
✅ **Reproducible**: Same commands work every time  
✅ **Automated**: Can be scripted or put in CI/CD  
✅ **Clean**: Service starts and stops in controlled manner  

## Environment Modes

- **Testing Mode** (`ML_USE_FALLBACK=true`): Uses TF-IDF, no model download needed
- **Production Mode** (default or `ML_USE_FALLBACK=false`): Uses sentence-transformers model
