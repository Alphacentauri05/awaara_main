"""
Bulk upload script for Cloudinary.
Because dragging files into a web UI is beneath you.
"""

import cloudinary
import cloudinary.uploader
from pathlib import Path
import argparse
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def upload_images(
    images_folder: str,
    cloud_name: str,
    api_key: str,
    api_secret: str,
    folder: str = "events"
):
    """
    Upload all images from a local folder to Cloudinary.
    
    Args:
        images_folder: Path to folder containing images
        cloud_name: Your Cloudinary cloud name
        api_key: Your Cloudinary API key
        api_secret: Your Cloudinary API secret
        folder: Cloudinary folder to upload to (default: events)
    """
    
    # Configure Cloudinary
    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret
    )
    
    print(f"Uploading images to Cloudinary...")
    print(f"Cloud: {cloud_name}")
    print(f"Folder: {folder}")
    print()
    
    # Supported image extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
    
    # Get all image files
    images_path = Path(images_folder)
    image_files = [
        f for f in images_path.iterdir()
        if f.is_file() and f.suffix.lower() in image_extensions
    ]
    
    print(f"Found {len(image_files)} images. Starting upload...")
    print()
    
    uploaded_count = 0
    failed_count = 0
    
    for img_file in image_files:
        try:
            result = cloudinary.uploader.upload(
                str(img_file),
                folder=folder,
                use_filename=True,
                unique_filename=False,
                overwrite=False  # Don't overwrite existing files
            )
            
            print(f"✓ {img_file.name}")
            print(f"  URL: {result['secure_url']}")
            uploaded_count += 1
            
        except Exception as e:
            print(f"✗ {img_file.name}")
            print(f"  Error: {str(e)}")
            failed_count += 1
    
    print()
    print(f"{'='*60}")
    print(f"Upload complete:")
    print(f"  - Uploaded: {uploaded_count}")
    print(f"  - Failed: {failed_count}")
    print(f"  - Total: {len(image_files)}")
    print(f"{'='*60}")
    print()
    print(f"Your Cloudinary base URL:")
    print(f"  https://res.cloudinary.com/{cloud_name}/image/upload/{folder}/")
    print()
    print(f"Use this URL when running generate_embeddings.py")

def main():
    parser = argparse.ArgumentParser(
        description="Upload images to Cloudinary"
    )
    parser.add_argument(
        "images_folder",
        help="Path to folder containing images"
    )
    parser.add_argument(
        "--cloud-name",
        default=os.getenv("CLOUDINARY_CLOUD_NAME"),
        help="Cloudinary cloud name (or set CLOUDINARY_CLOUD_NAME in .env)"
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("CLOUDINARY_API_KEY"),
        help="Cloudinary API key (or set CLOUDINARY_API_KEY in .env)"
    )
    parser.add_argument(
        "--api-secret",
        default=os.getenv("CLOUDINARY_API_SECRET"),
        help="Cloudinary API secret (or set CLOUDINARY_API_SECRET in .env)"
    )
    parser.add_argument(
        "--folder",
        default="events",
        help="Cloudinary folder to upload to (default: events)"
    )
    
    args = parser.parse_args()
    
    # Validate credentials are provided
    if not args.cloud_name or not args.api_key or not args.api_secret:
        print("Error: Cloudinary credentials missing!")
        print("Either:")
        print("  1. Create a .env file with CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET")
        print("  2. Pass credentials via command-line: --cloud-name --api-key --api-secret")
        return
    
    # Validate inputs
    if not os.path.isdir(args.images_folder):
        print(f"Error: '{args.images_folder}' is not a valid directory.")
        return
    
    upload_images(
        args.images_folder,
        args.cloud_name,
        args.api_key,
        args.api_secret,
        args.folder
    )

if __name__ == "__main__":
    main()
