"""
FastAPI backend for finding faces in event photos.
Because apparently you need AI to find yourself in pictures.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json
import io
from PIL import Image
import insightface
from insightface.app import FaceAnalysis
from typing import List
import os

# Initialize FastAPI with a disappointed tone
app = FastAPI(
    title="Find My Photos API",
    description="Because you can't recognize your own face.",
    version="1.0.0"
)

# CORS - allowing everything because security is someone else's problem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response models because type safety matters (allegedly)
class MatchResult(BaseModel):
    imageUrl: str
    score: float

class FindResponse(BaseModel):
    matches: List[MatchResult]

# Global variables - load once because we're not wasteful
face_analyzer = None
embeddings_data = []

@app.on_event("startup")
async def load_models_and_data():
    """
    Load InsightFace model and embeddings on startup.
    This takes forever but at least it only happens once.
    """
    global face_analyzer, embeddings_data
    
    print("Loading face recognition model... this will take a minute because of course it does.")
    
    # Initialize InsightFace
    face_analyzer = FaceAnalysis(
        name='buffalo_sc',  # Using buffalo_sc (super compact) - fits in 512 MB free tier
        providers=['CPUExecutionProvider']  # CPU only because you're probably on a free tier
    )
    face_analyzer.prepare(ctx_id=0, det_size=(640, 640))
    
    print("Model loaded. Now loading embeddings...")
    
    # Load embeddings from JSON file
    embeddings_path = os.path.join(os.path.dirname(__file__), "embeddings1.json")
    
    if not os.path.exists(embeddings_path):
        print(f"WARNING: {embeddings_path} not found. Creating empty file.")
        with open(embeddings_path, "w") as f:
            json.dump([], f)
        embeddings_data = []
    else:
        with open(embeddings_path, "r") as f:
            embeddings_data = json.load(f)
        print(f"Loaded {len(embeddings_data)} embeddings. Assuming they're actually valid.")
    
    print("Startup complete. Ready to disappoint users.")

@app.get("/")
async def root():
    """
    Health check endpoint.
    """
    return {
        "message": "API is running. Surprisingly.",
        "total_embeddings": len(embeddings_data)
    }

@app.post("/find", response_model=FindResponse)
async def find_face(file: UploadFile = File(...)):
    """
    Find photos containing the uploaded face.
    
    Steps:
    1. Read uploaded image (assuming you uploaded something valid)
    2. Detect face (assuming you sent a photo with an actual face)
    3. Compute embedding
    4. Compare with all stored embeddings
    5. Return top matches sorted by similarity
    
    Returns 400 if no face detected.
    Returns 500 if something breaks (inevitable).
    """
    global face_analyzer, embeddings_data
    
    if face_analyzer is None:
        raise HTTPException(
            status_code=500,
            detail="Model not loaded yet. Server crashed. Predictable."
        )
    
    if not embeddings_data:
        raise HTTPException(
            status_code=400,
            detail="No embeddings available. Did you forget to generate embeddings.json?"
        )
    
    try:
        # Read uploaded file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Convert to RGB if needed (because you probably sent a PNG with alpha channel)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert PIL Image to numpy array for InsightFace
        img_array = np.array(image)
        
        # Detect faces
        faces = face_analyzer.get(img_array)
        
        if len(faces) == 0:
            raise HTTPException(
                status_code=400,
                detail="No face detected. Somehow even the model gave up on you."
            )
        
        # Use the first face (assuming you sent a selfie with ONE face)
        query_embedding = faces[0].embedding
        
        # Normalize embedding (InsightFace embeddings should already be normalized, but just in case)
        query_embedding = query_embedding / np.linalg.norm(query_embedding)
        
        # Extract all embeddings from stored data
        stored_embeddings = np.array([item["embedding"] for item in embeddings_data])
        
        # Compute cosine similarity
        # Reshape query to (1, n_features) for sklearn
        similarities = cosine_similarity(
            query_embedding.reshape(1, -1),
            stored_embeddings
        )[0]
        
        # Get indices sorted by similarity (descending)
        sorted_indices = np.argsort(similarities)[::-1]
        
        # Get top N matches (let's say top 20, or all if fewer)
        top_n = 20
        top_indices = sorted_indices[:top_n]
        
        # Filter by minimum similarity threshold (e.g., 0.3)
        # Because showing random unrelated photos is useless
        min_similarity = 0.3
        matches = []
        
        for idx in top_indices:
            score = float(similarities[idx])
            if score >= min_similarity:
                matches.append(MatchResult(
                    imageUrl=embeddings_data[idx]["imageUrl"],
                    score=score
                ))
        
        return FindResponse(matches=matches)
    
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Catch any other errors because things will break
        print(f"Error processing request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Server crashed. Predictable. Error: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """
    Health check for deployment platforms.
    """
    return {
        "status": "alive",
        "embeddings_count": len(embeddings_data),
        "model_loaded": face_analyzer is not None
    }
