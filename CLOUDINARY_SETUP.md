# Cloudinary Setup Guide

A step-by-step guide for setting up Cloudinary to host your event photos. Follow this because you'll probably mess it up otherwise.

---

## Step 1: Create Cloudinary Account

1. Go to **https://cloudinary.com/users/register/free**
2. Sign up with:
   - Email address
   - Password
   - Or use Google/GitHub sign-in (easier)
3. Verify your email if prompted
4. You'll be redirected to the Cloudinary dashboard

**Free tier includes:**
- 25 GB storage
- 25 GB bandwidth per month
- 25,000 transformations per month

More than enough for a hobby project.

---

## Step 2: Get Your Cloudinary Credentials

Once logged in:

1. **Go to the Dashboard** (should be the default landing page)
2. You'll see a **"Product Environment Credentials"** section with:
   - **Cloud Name** (e.g., `dzabcdefgh`)
   - **API Key** (e.g., `123456789012345`)
   - **API Secret** (e.g., `abcdefghijklmnopqrstuvwxyz-123`)

3. **Copy these values NOW**. Don't skip this. Put them somewhere safe like:
   - A password manager
   - A local text file (NOT committed to git)
   - Your notes app

You'll need these for:
- Uploading images
- Generating embeddings
- (Optional) Backend API if you extend the app

---

## Step 3: Create a Folder for Event Photos (Optional but Recommended)

Organizing your images makes life easier.

1. Click **"Media Library"** in the left sidebar
2. Click **"New Folder"** button (top right area)
3. Name it: `events` (or whatever you want)
4. Click "Create"

Now you have a dedicated folder for event photos.

**Why do this?**
- Keeps things organized
- Multiple events can have subfolders: `events/wedding`, `events/party`
- Easier to manage URLs

---

## Step 4: Upload Your Event Photos

You have **three options**. Pick one.

### Option A: Web Dashboard (Easiest for < 50 photos)

1. Go to **Media Library**
2. Open your `events` folder (if you created one)
3. Click **"Upload"** button
4. Select your event photos from your computer
5. Wait for upload to complete
6. Done. Images are now hosted on Cloudinary's CDN.

**Pros:** Simple, visual, no code  
**Cons:** Tedious for hundreds of photos

---

### Option B: Python Upload Script (Recommended for bulk)

I already created this script for you: `backend/upload_to_cloudinary.py`

1. **Install Cloudinary SDK:**
   ```bash
   cd backend
   pip install cloudinary
   ```

2. **Run the upload script:**
   ```bash
   python upload_to_cloudinary.py /path/to/your/photos \
     --cloud-name YOUR_CLOUD_NAME \
     --api-key YOUR_API_KEY \
     --api-secret YOUR_API_SECRET \
     --folder events
   ```

   **Replace:**
   - `/path/to/your/photos` → actual path to folder with images
   - `YOUR_CLOUD_NAME` → from Step 2
   - `YOUR_API_KEY` → from Step 2
   - `YOUR_API_SECRET` → from Step 2

3. **Example:**
   ```bash
   python upload_to_cloudinary.py ./my_event_photos \
     --cloud-name dzabcdefgh \
     --api-key 123456789012345 \
     --api-secret abcdefghijklmnopqrstuvwxyz-123 \
     --folder events
   ```

4. Script will output each uploaded image URL. **Save the base URL** from the output:
   ```
   Your Cloudinary base URL:
     https://res.cloudinary.com/dzabcdefgh/image/upload/events/
   ```

**Pros:** Fast, handles many files, shows progress  
**Cons:** Requires Python

---

### Option C: Cloudinary CLI (For Power Users)

If you prefer command-line tools:

1. **Install Cloudinary CLI:**
   ```bash
   npm install -g cloudinary-cli
   ```

2. **Configure with credentials:**
   ```bash
   cld config
   ```
   Enter your Cloud Name, API Key, and API Secret when prompted.

3. **Upload images:**
   ```bash
   cld uploader upload ./your-photos-folder/* folder=events
   ```

**Pros:** Official tool, handles everything  
**Cons:** Requires Node.js

---

## Step 5: Construct Your Cloudinary Base URL

After uploading, you need to know your **Cloudinary Base URL** for the next steps.

**Format:**
```
https://res.cloudinary.com/<CLOUD_NAME>/image/upload/<FOLDER>/
```

**Examples:**

If your cloud name is `dzabcdefgh` and folder is `events`:
```
https://res.cloudinary.com/dzabcdefgh/image/upload/events/
```

If no folder (uploaded to root):
```
https://res.cloudinary.com/dzabcdefgh/image/upload/
```

**IMPORTANT:** The URL must end with `/` (trailing slash).

**Test your URL:**
Pick one image you uploaded, e.g., `photo1.jpg`. The full URL should be:
```
https://res.cloudinary.com/dzabcdefgh/image/upload/events/photo1.jpg
```

Paste this in your browser. If the image loads, you configured it correctly.

---

## Step 6: Generate Face Embeddings

Now that images are uploaded to Cloudinary, generate the embeddings file.

1. **Make sure you have the photos locally too** (same folder you uploaded from)

2. **Run the embedding generation script:**
   ```bash
   cd backend
   python generate_embeddings.py /path/to/local/photos "YOUR_CLOUDINARY_BASE_URL"
   ```

   **Example:**
   ```bash
   python generate_embeddings.py ./my_event_photos \
     "https://res.cloudinary.com/dzabcdefgh/image/upload/events/"
   ```

3. **What this does:**
   - Loads the InsightFace AI model (takes 1-2 min first time)
   - Processes each image
   - Detects faces
   - Generates 512-dimensional embedding for each face
   - Saves to `embeddings.json` with Cloudinary URLs

4. **Output:**
   ```
   Processing complete:
     - Images processed: 42 / 42
     - Total faces found: 127
     - Output file: /path/to/backend/embeddings.json
   ```

5. **Verify embeddings.json:**
   Open `backend/embeddings.json` and check:
   - URLs point to your Cloudinary images
   - Embeddings are arrays of numbers (512 floats each)
   - File size is reasonable (not just dummy data)

---

## Step 7: Verify Everything Works

Before deploying, test locally:

1. **Start backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app:app --reload --port 8000
   ```

2. **Start frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Test the app:**
   - Go to `http://localhost:3000`
   - Upload a selfie of someone who's in the event photos
   - Click "Search My Face"
   - Should return matching photos from Cloudinary

If it works, you're done with setup!

---

## Troubleshooting

### "No face detected" error
- Make sure uploaded selfie is clear and face is visible
- Avoid sunglasses, masks, or extreme angles

### Empty results (no matches found)
- Check that embeddings.json has real data (not dummy examples)
- Verify Cloudinary URLs in embeddings.json work (paste in browser)
- Ensure filenames match between local files and Cloudinary uploads

### "embeddings.json not found" or is empty
- You didn't run `generate_embeddings.py`
- Run it now with correct paths and Cloudinary base URL

### Images not loading in frontend
- Check Next.js config allows remote images (already configured)
- Verify Cloudinary URLs are public (they should be by default)
- Check browser console for CORS errors (shouldn't happen with Cloudinary)

### Upload script errors
- Double-check your API credentials
- Make sure folder path exists locally
- Check internet connection

---

## Summary Checklist

- [ ] Created Cloudinary account
- [ ] Saved Cloud Name, API Key, API Secret
- [ ] Created `events` folder in Media Library
- [ ] Uploaded event photos to Cloudinary
- [ ] Noted Cloudinary base URL
- [ ] Ran `generate_embeddings.py` with local photos and Cloudinary URL
- [ ] Verified `embeddings.json` has real data (not dummy examples)
- [ ] Tested app locally with a selfie
- [ ] Got results showing Cloudinary-hosted images

If all checkboxes are checked, you're ready to deploy.

---

## Next Steps

After Cloudinary setup is complete:
1. Deploy backend to Render (see main README.md)
2. Deploy frontend to Vercel (see main README.md)
3. Add more event photos as needed (repeat Steps 4 & 6)

Good luck. You'll need it.
