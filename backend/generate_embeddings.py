"""
Script to generate embeddings.json from a folder of event photos.
Run this locally or on server to build your embeddings database.

Because you definitely can't do this manually.
"""

import os
import json
import numpy as np
from PIL import Image
import insightface
from insightface.app import FaceAnalysis
from pathlib import Path
import argparse

def generate_embeddings(
    images_folder: str,
    cloudinary_base_url: str,
    output_file: str = "embeddings.json"
):
    """
    Generate embeddings for all images in a folder.
    
    Args:
        images_folder: Path to folder containing event photos
        cloudinary_base_url: Base URL for Cloudinary (e.g., "https://res.cloudinary.com/your-cloud/image/upload/events/")
        output_file: Output JSON file path (default: embeddings.json)
    
    This will:
    1. Load InsightFace model (wait forever)
    2. Iterate through all images
    3. Detect faces in each image
    4. Generate embeddings for each face
    5. Save to JSON with Cloudinary URLs
    """
    
    print("Initializing face recognition model... grab a coffee, this takes forever.")
    
    # Initialize InsightFace
    face_analyzer = FaceAnalysis(
        name='buffalo_l',
        providers=['CPUExecutionProvider']
    )
    face_analyzer.prepare(ctx_id=0, det_size=(640, 640))
    
    print("Model loaded. Processing images...")
    
    # List to store all embeddings
    embeddings_list = []
    
    # Supported image extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
    
    # Get all image files in folder
    images_path = Path(images_folder)
    image_files = [
        f for f in images_path.iterdir()
        if f.is_file() and f.suffix.lower() in image_extensions
    ]
    
    print(f"Found {len(image_files)} images. Processing...")
    
    processed_count = 0
    faces_found = 0
    
    for img_file in image_files:
        try:
            # Load image
            image = Image.open(img_file)
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to numpy array
            img_array = np.array(image)
            
            # Detect faces
            faces = face_analyzer.get(img_array)
            
            if len(faces) == 0:
                print(f"  ⚠️  No faces found in {img_file.name}")
                continue
            
            # Process each detected face
            for face_idx, face in enumerate(faces):
                # Get embedding
                embedding = face.embedding.tolist()
                
                # Construct Cloudinary URL
                # Assuming you upload images with the same filename to Cloudinary
                image_url = f"{cloudinary_base_url}{img_file.name}"
                
                # Add to list
                embeddings_list.append({
                    "imageUrl": image_url,
                    "embedding": embedding
                })
                
                faces_found += 1
                print(f"  ✓ Processed {img_file.name} - found {len(faces)} face(s)")
            
            processed_count += 1
            
        except Exception as e:
            print(f"  ✗ Error processing {img_file.name}: {str(e)}")
            continue
    
    # Save to JSON
    output_path = Path(output_file)
    with open(output_path, 'w') as f:
        json.dump(embeddings_list, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"Processing complete:")
    print(f"  - Images processed: {processed_count} / {len(image_files)}")
    print(f"  - Total faces found: {faces_found}")
    print(f"  - Output file: {output_path.absolute()}")
    print(f"{'='*60}")
    print(f"\nNow upload your images to Cloudinary and make sure the base URL matches:")
    print(f"  {cloudinary_base_url}")
    print(f"\nIf you screw up the URL, nothing will work. Don't say I didn't warn you.")

def main():
    parser = argparse.ArgumentParser(
        description="Generate embeddings.json from event photos"
    )
    parser.add_argument(
        "images_folder",
        help="Path to folder containing event photos"
    )
    parser.add_argument(
        "cloudinary_base_url",
        help='Base URL for Cloudinary (e.g., "https://res.cloudinary.com/your-cloud/image/upload/events/")'
    )
    parser.add_argument(
        "--output",
        default="embeddings.json",
        help="Output file path (default: embeddings.json)"
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    if not os.path.isdir(args.images_folder):
        print(f"Error: '{args.images_folder}' is not a valid directory.")
        return
    
    if not args.cloudinary_base_url.startswith("http"):
        print(f"Warning: Cloudinary base URL should start with http:// or https://")
        print(f"You provided: {args.cloudinary_base_url}")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    generate_embeddings(
        args.images_folder,
        args.cloudinary_base_url,
        args.output
    )

if __name__ == "__main__":
    main()
