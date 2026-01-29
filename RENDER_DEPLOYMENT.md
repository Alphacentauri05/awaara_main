`# Render Deployment Guide

This guide will help you deploy your **awaara-web-app** backend to Render without size issues.

## 🎯 What We've Fixed

1. **Excluded Large/Unnecessary Files from Git:**
   - `backend/generate_embeddings.py` - Only needed locally to generate embeddings
   - `backend/upload_to_cloudinary.py` - Only needed locally to upload images
   - `Event1/` folder - Contains large image files (already on Cloudinary)
   - All `Event*/` folders - Other event photo folders

2. **What Gets Deployed:**
   - Only the essential backend code (`app.py`)
   - Dependencies (`requirements.txt`, `runtime.txt`)
   - Pre-generated `embeddings.json` file
   - Environment configuration

## 📋 Pre-Deployment Checklist

### 1. Ensure embeddings.json Exists
Before deploying, make sure `backend/embeddings.json` exists with your photo embeddings:

```bash
# If you haven't generated embeddings yet, run locally:
cd backend
python generate_embeddings.py
```

> **Important:** The `embeddings.json` file should be committed to Git. This file is small and contains only the numeric embeddings, not the actual photos.

### 2. Commit Your Changes

```bash
# Stage the updated .gitignore
git add .gitignore

# Make sure embeddings.json is tracked (not ignored)
git add backend/embeddings.json

# Stage your backend code
git add backend/app.py backend/requirements.txt backend/runtime.txt

# Commit (utility scripts and Event folders will be auto-excluded)
git commit -m "Optimize for Render deployment"

# Push to GitHub
git push origin main
```

## 🚀 Deploying to Render

### Option 1: Using render.yaml (Recommended)

Your project already has a `render.yaml` configuration file. Here's how to deploy:

1. **Go to [Render Dashboard](https://dashboard.render.com/)**

2. **Create New > Blueprint**
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`
   - Click **"Apply"**

3. **Set Environment Variables** in the Render dashboard:
   ```
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   FRONTEND_URL=https://your-frontend-url.vercel.app
   ```

### Option 2: Manual Setup

1. **Go to Render Dashboard > New > Web Service**

2. **Connect Repository:**
   - Select your `awaara-web-app` repository
   - Branch: `main`

3. **Configure Service:**
   - **Name:** `awaara-backend` (or your preferred name)
   - **Region:** Choose closest to your users
   - **Root Directory:** `backend`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app:app --host 0.0.0.0 --port 10000`

4. **Environment Variables:**
   Add the following in the "Environment" section:
   ```
   PYTHON_VERSION=3.11.9
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   FRONTEND_URL=https://your-frontend-url.vercel.app
   ```

5. **Advanced Settings:**
   - **Health Check Path:** `/health`
   - **Auto-Deploy:** Yes (deploys on every git push)

6. **Click "Create Web Service"**

## 🔍 Troubleshooting

### "Size Exceeded" Error
✅ **Fixed!** By excluding the following from Git:
- `Event1/` and other event folders (large image files)
- Utility scripts that are only needed locally
- Development files already in `.gitignore`

### Build Fails
- Check that `backend/embeddings.json` exists in your repository
- Verify all environment variables are set correctly
- Check Render logs for specific error messages

### Application Won't Start
- Ensure the start command is: `uvicorn app:app --host 0.0.0.0 --port 10000`
- Verify Python version matches `runtime.txt`: `python-3.11.9`
- Check that all dependencies in `requirements.txt` are compatible

### CORS Errors
- Make sure `FRONTEND_URL` environment variable is set correctly
- Update it when you deploy your frontend

## 📊 Post-Deployment

### Get Your Backend URL
After deployment, Render will provide a URL like:
```
https://awaara-backend.onrender.com
```

### Update Frontend Configuration
Update your frontend's API endpoint to point to your Render backend URL.

### Test the Deployment
```bash
# Health check
curl https://your-backend-url.onrender.com/health

# Should return: {"status": "healthy"}
```

## 🔄 Future Deployments

Once set up, deploying is automatic:

1. Make code changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your changes"
   git push origin main
   ```
3. Render automatically deploys! 🎉

## 💡 Tips

- **Free Tier Limitation:** Render free tier spins down after inactivity. First request may take 30-60 seconds.
- **Keep embeddings.json Updated:** When you add new photos, regenerate embeddings locally and commit the updated file.
- **Monitor Logs:** Use Render dashboard to view real-time logs and debug issues.

## 📁 Files Excluded from Deployment

These files remain on your local machine only:
- ❌ `backend/generate_embeddings.py`
- ❌ `backend/upload_to_cloudinary.py`
- ❌ `Event1/` folder and all images
- ✅ `backend/embeddings.json` - **This IS included** (small, essential)

---

**Ready to Deploy!** Follow the steps above and your backend will be live on Render without size issues. 🚀
