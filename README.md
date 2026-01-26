# Find My Photos

A face recognition app that finds photos containing your face from event photo collections. Because apparently you need AI to recognize yourself.

> **📖 Quick Start:** New to Cloudinary? Read [CLOUDINARY_SETUP.md](./CLOUDINARY_SETUP.md) for step-by-step setup instructions.

## Tech Stack

**Frontend:**
- Next.js 14 (App Router) + TypeScript
- Tailwind CSS
- Deployed on Vercel

**Backend:**
- Python 3.11 + FastAPI
- InsightFace for face recognition
- NumPy + scikit-learn for similarity matching
- Deployed on Render

**Storage:**
- Cloudinary for event photos
- JSON file for face embeddings (no database)

---

## Folder Structure

```
/
├── frontend/              # Next.js application
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx          # Main page
│   │   │   ├── layout.tsx        # Root layout
│   │   │   └── globals.css       # Global styles
│   │   └── components/
│   │       ├── UploadForm.tsx    # File upload component
│   │       └── ResultsGrid.tsx   # Results display
│   ├── package.json
│   ├── next.config.mjs
│   ├── tailwind.config.mjs
│   └── tsconfig.json
│
├── backend/               # FastAPI application
│   ├── app.py                    # Main API server
│   ├── generate_embeddings.py   # Script to generate embeddings.json
│   ├── embeddings.json          # Face embeddings database
│   └── requirements.txt         # Python dependencies
│
├── render.yaml            # Render deployment config
└── README.md             # This file
```

---

## Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- A Cloudinary account (for image hosting)
- A Render account (for backend deployment)
- A Vercel account (for frontend deployment)

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd awaara_web_main
```

### 2. Set Up Cloudinary

**Why Cloudinary?** It's a dedicated image/video management platform with generous free tier and built-in CDN.

#### Step-by-step:

1. **Create a Cloudinary account** at https://cloudinary.com/users/register/free
2. **Get your credentials** from the dashboard:
   - Go to "Dashboard" after signing in
   - You'll see your account details:
     - **Cloud Name** (e.g., `dzabcdefgh`)
     - **API Key** (e.g., `123456789012345`)
     - **API Secret** (e.g., `abcdefghijklmnopqrstuvwxyz`)
   - Save these - you'll need them
3. **Create a folder for your event photos** (optional but recommended):
   - Go to "Media Library"
   - Click "Create Folder"
   - Name it `events` or whatever you want
   - This helps organize your images

Your **Cloudinary base URL** format will be:
```
https://res.cloudinary.com/<cloud_name>/image/upload/
```

For example, if your cloud name is `dzabcdefgh`:
```
https://res.cloudinary.com/dzabcdefgh/image/upload/events/
```

### 3. Upload Event Photos to Cloudinary

You have three options:

#### Option A: Use Cloudinary Dashboard (easiest for small batches)
1. Go to your Cloudinary Media Library
2. Click "Upload" button
3. Select your event photos
4. Optionally upload to a specific folder (e.g., `events/`)
5. Images will be available immediately via CDN

#### Option B: Use Upload Script (recommended for bulk uploads)

Create a simple upload script using the Cloudinary Python SDK:

```bash
# Install Cloudinary SDK
pip install cloudinary
```

Then create `backend/upload_to_cloudinary.py`:
```python
import cloudinary
import cloudinary.uploader
from pathlib import Path
import os

# Configure Cloudinary
cloudinary.config(
    cloud_name="YOUR_CLOUD_NAME",
    api_key="YOUR_API_KEY",
    api_secret="YOUR_API_SECRET"
)

# Upload all images from a folder
folder_path = "./your-photos-folder"
for img_file in Path(folder_path).glob("*.jpg"):
    result = cloudinary.uploader.upload(
        str(img_file),
        folder="events",  # Optional: organize in folders
        use_filename=True,
        unique_filename=False
    )
    print(f"Uploaded: {img_file.name} -> {result['secure_url']}")
```

#### Option C: Use Cloudinary CLI (for power users)

Install and use the official CLI:
```bash
npm install -g cloudinary-cli
cld config
# Follow prompts to enter your credentials
cld uploader upload ./your-photos-folder/* folder=events
```

### 4. Generate Face Embeddings

After uploading photos to Cloudinary, generate the embeddings file:

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Run the embedding generation script
python generate_embeddings.py \
  /path/to/local/photos \
  "https://res.cloudinary.com/YOUR_CLOUD_NAME/image/upload/events/"

# Example:
# python generate_embeddings.py ./event_photos "https://res.cloudinary.com/dzabcdefgh/image/upload/events/"
```

**Important:**
- The first argument is the path to your **local** folder with event photos
- The second argument is your **Cloudinary base URL** (must end with `/`)
- Format: `https://res.cloudinary.com/<cloud_name>/image/upload/<optional_folder>/`
- This will create `embeddings.json` in the backend folder
- Make sure the Cloudinary base URL matches where you uploaded the images

The script will:
1. Load the InsightFace model (takes 1-2 minutes)
2. Process each image
3. Detect faces
4. Generate 512-dimensional embeddings
5. Save to `embeddings.json` with Cloudinary URLs

**Note:** The script processes images from your local folder and generates URLs pointing to Cloudinary. Make sure you've uploaded the images to Cloudinary with the same filenames.

### 5. Backend Setup (Local Development)

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`

**First startup will be slow** (1-2 minutes) because InsightFace downloads its models.

Test it:
```bash
curl http://localhost:8000/health
```

Should return:
```json
{
  "status": "alive",
  "embeddings_count": <number>,
  "model_loaded": true
}
```

### 6. Frontend Setup (Local Development)

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.local.example .env.local

# Edit .env.local and set:
# NEXT_PUBLIC_BACKEND_URL=http://localhost:8000

# Run development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 7. Test Locally

1. Open `http://localhost:3000`
2. Upload a selfie
3. Click "Search My Face"
4. Wait for results (or error messages, more likely)

---

## Deployment

### Deploy Backend to Render

1. **Push your code to GitHub** (or GitLab/Bitbucket)

2. **Create a Render account** at https://render.com

3. **Create a new Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect `render.yaml` and configure the service
   
   **OR manually configure:**
   - Name: `find-my-photos-backend`
   - Environment: `Python 3`
   - Region: Choose closest to your users
   - Branch: `main`
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app:app --host 0.0.0.0 --port 10000`

4. **Deploy!** Render will build and deploy your backend.

5. **Note your backend URL:**
   ```
   https://find-my-photos-backend.onrender.com
   ```
   (Your actual URL will be different)

**Important:** First request after deployment will be SLOW (30-60 seconds) because:
- Free tier spins down after inactivity
- InsightFace downloads models on first run

Consider keeping it awake with a cron job pinging `/health` every 10 minutes.

**Note:** If you want to use Cloudinary SDK in the backend (for dynamic uploads), add environment variables in Render:
- `CLOUDINARY_CLOUD_NAME`
- `CLOUDINARY_API_KEY`
- `CLOUDINARY_API_SECRET`

But this app doesn't need them since images are referenced by public URL.

### Deploy Frontend to Vercel

1. **Create a Vercel account** at https://vercel.com

2. **Import your repository:**
   - Click "Add New..." → "Project"
   - Import your GitHub repository
   - Vercel will auto-detect Next.js

3. **Configure build settings:**
   - Framework Preset: `Next.js`
   - Root Directory: `frontend`
   - Build Command: `npm run build` (default)
   - Output Directory: `.next` (default)

4. **Add environment variable:**
   - In project settings → "Environment Variables"
   - Add:
     ```
     NEXT_PUBLIC_BACKEND_URL=https://find-my-photos-backend.onrender.com
     ```
   - Replace with your actual Render backend URL

5. **Deploy!** Vercel will build and deploy your frontend.

6. **Your app is live at:**
   ```
   https://your-project.vercel.app
   ```

---

## Environment Variables

### Frontend (.env.local)

```bash
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000  # Development
# NEXT_PUBLIC_BACKEND_URL=https://your-backend.onrender.com  # Production
```

### Backend (Optional Cloudinary env vars)

Everything is in `embeddings.json`. If you want to use Cloudinary SDK for programmatic uploads (not needed for this app), you'd add:
```bash
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

But this app doesn't need them because images are referenced by public URL in embeddings.json.

---

## API Documentation

### POST /find

Upload a selfie and find matching event photos.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `file` (image file)

**Response (Success):**
```json
{
  "matches": [
    {
      "imageUrl": "https://res.cloudinary.com/your-cloud/image/upload/events/photo1.jpg",
      "score": 0.9234
    },
    {
      "imageUrl": "https://res.cloudinary.com/your-cloud/image/upload/events/photo2.jpg",
      "score": 0.8876
    }
  ]
}
```

**Response (No face detected):**
```json
{
  "detail": "No face detected. Somehow even the model gave up on you."
}
```
Status: 400

**Response (Server error):**
```json
{
  "detail": "Server crashed. Predictable."
}
```
Status: 500

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "alive",
  "embeddings_count": 42,
  "model_loaded": true
}
```

---

## Troubleshooting

### "No face detected"
- Make sure you're uploading a clear selfie with your face visible
- Face should be reasonably sized in the frame
- Avoid sunglasses, masks, or extreme angles

### "Server crashed"
- Check Render logs for actual error
- Likely causes:
  - InsightFace model failed to load (out of memory on free tier)
  - `embeddings.json` is malformed
  - Image format not supported

### Empty results
- Your face might not be in the uploaded event photos
- Embeddings threshold might be too high (edit `min_similarity` in `app.py`)
- Embeddings were generated from different photos than what's uploaded to Cloudinary
- Cloudinary URLs in embeddings.json might be incorrect

### Slow backend response
- First request after inactivity takes 30-60s on Render free tier
- Model loading takes time
- Consider upgrading to paid tier or keeping service awake

### CORS errors
- Make sure `NEXT_PUBLIC_BACKEND_URL` is set correctly
- Backend allows all origins by default (see `app.py` CORS config)
- In production, restrict to your Vercel domain

---

## Updating Embeddings

When you add new event photos:

1. Upload new photos to Cloudinary
2. Run `generate_embeddings.py` again with ALL photos (including old ones)
3. Replace `embeddings.json` in the backend folder
4. Redeploy backend to Render (or restart the service)

**Or** if you're clever, modify the script to append to existing `embeddings.json`.

---

## Cost Estimate (Free Tiers)

- **Cloudinary:** 25 GB storage, 25 GB bandwidth/month free
- **Render:** 750 hours/month free for web services
- **Vercel:** Unlimited for personal projects

**Realistic monthly cost for hobby project:** $0

**If you exceed free tiers:** Cloudinary ~$0.10/GB, Render starts at $7/month

---

## Known Limitations

- Single-face detection in uploaded selfie (uses first detected face)
- Linear search through embeddings (slow for >10k images)
- No authentication (anyone can query)
- No rate limiting (can be abused)
- Free tier cold starts take 30-60s
- InsightFace model is large (~200MB download on first run)

**If you need better:**
- Use a vector database (Pinecone, Qdrant, Weaviate)
- Add authentication
- Implement caching
- Use GPU for faster inference
- Add rate limiting

But you probably don't need any of that.

---

## Development Notes

### File Structure Explanation

- **embeddings.json:** Contains face embeddings (512-float arrays) + Cloudinary URLs
- **generate_embeddings.py:** One-time script to process images and create embeddings.json
- **app.py:** FastAPI server that loads embeddings into memory on startup
- **No database:** Everything in JSON because simplicity > performance for small datasets

### Adding More Event Collections

To support multiple events:
1. Organize Cloudinary with folders: `events/wedding/`, `events/party/`
2. Modify `embeddings.json` to include event metadata
3. Add event filtering to API
4. Update frontend to select event

But that's your problem, not mine.

---

## License

Do whatever you want with this code. No guarantees it works.

---

## Support

If this doesn't work, it's probably your fault. Check:
1. Did you actually upload images to Cloudinary?
2. Does your Cloudinary base URL match the format `https://res.cloudinary.com/<cloud_name>/image/upload/`?
3. Did you run `generate_embeddings.py`?
4. Is `embeddings.json` valid JSON?
5. Are your environment variables set correctly?

If all else fails, read the error messages. They're pretty explicit about what went wrong.

Good luck. You'll need it.
