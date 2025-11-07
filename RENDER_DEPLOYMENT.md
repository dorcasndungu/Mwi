# Render Deployment Guide

## ⚠️ Important: Python Version Configuration

Render may auto-detect Poetry or use the latest Python version. To ensure Python 3.9.18 is used:

### Option 1: Using runtime.txt (Recommended)
The `runtime.txt` file should automatically set Python 3.9.18. If Render is still using Python 3.13:

1. Go to your Render Dashboard
2. Select your service
3. Go to **Settings** → **Environment**
4. Manually set **Python Version** to `3.9.18`
5. Save and redeploy

### Option 2: Manual Configuration in Render Dashboard

If `render.yaml` is not being used:

1. **Runtime**: Python 3.9.18
2. **Build Command**: 
   ```bash
   pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
   ```
3. **Start Command**: 
   ```bash
   gunicorn --bind 0.0.0.0:$PORT app:app --timeout 300 --workers 2 --preload
   ```

## 🔧 Troubleshooting

### Issue: Pillow build fails with Python 3.13
**Solution**: The `runtime.txt` file forces Python 3.9.18. If Render still uses 3.13, manually set it in the dashboard.

### Issue: Render using Poetry
**Solution**: If Render detects Poetry, it will ignore `requirements.txt`. Make sure there's no `pyproject.toml` or `poetry.lock` file in your repo.

### Issue: Build timeout
**Solution**: Face recognition libraries (dlib) can take 15-20 minutes. The build command has a fallback that installs core dependencies if face recognition fails.

## ✅ Verification

After deployment, check:
- `/health` - Should return "OK"
- `/api/status` - Shows if face recognition is available or running in demo mode

