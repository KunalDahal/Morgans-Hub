# hash.py (updated)
import hashlib
import os
import json
import logging
import tempfile
from PIL import Image, UnidentifiedImageError
import imagehash
import io
from moviepy import VideoFileClip
from typing import List, Dict
from util import HASH_FILE, FILE_SIZE_LIMIT

logger = logging.getLogger(__name__)

def normalize_image(img_bytes: bytes) -> Image.Image:
    """Normalize image for consistent hashing"""
    try:
        img = Image.open(io.BytesIO(img_bytes))
        img = img.convert("RGB")
        img = img.resize((256, 256))
        return img
    except Exception as e:
        logger.error(f"Error normalizing image: {e}")
        raise

def compute_video_hashes(video_path: str) -> Dict:
    """Compute all hashes for a video by sampling frames"""
    try:
        clip = VideoFileClip(video_path)
        end_time = min(10, clip.duration)  # Use first 10 seconds or full video if shorter
        phashes = []
        dhashes = []
        ahashes = []
        
        # Sample frames at 2fps
        for t, img in clip.iter_frames(fps=2, with_times=True):
            if t > end_time:
                break
            try:
                pil_img = Image.fromarray(img)
                # Generate all hash types for each frame
                phashes.append(imagehash.phash(pil_img))
                dhashes.append(imagehash.dhash(pil_img))
                ahashes.append(imagehash.average_hash(pil_img))
            except Exception as e:
                logger.error(f"Error processing video frame: {e}")
                continue
        
        clip.close()
        
        if not phashes:
            return {}
            
        # Combine frame hashes by averaging
        avg_phash = str(imagehash.average_hash(phashes))
        avg_dhash = str(imagehash.average_hash(dhashes))
        avg_ahash = str(imagehash.average_hash(ahashes))
        
        return {
            'phash': avg_phash,
            'dhash': avg_dhash,
            'ahash': avg_ahash
        }
    except Exception as e:
        logger.error(f"Error computing video hashes: {e}")
        return {}

def _load_hash_data() -> Dict:
    try:
        if os.path.exists(HASH_FILE):
            with open(HASH_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error loading hash data: {e}")
    return {}

def _save_hash_data(hash_data: Dict):
    try:
        with open(HASH_FILE, 'w') as f:
            json.dump(hash_data, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving hash data: {e}")

def hamming_distance(hash1: str, hash2: str) -> int:
    """Calculate Hamming distance between two hashes"""
    if not hash1 or not hash2:
        return float('inf')
    return bin(int(hash1, 16) ^ int(hash2, 16)).count('1')

async def generate_media_hashes(message) -> List[Dict]:
    media_hashes = []
    
    if not hasattr(message, 'media') or not message.media:
        return media_hashes

    try:
        media_type = None
        file_size = 0
        
        if hasattr(message, 'photo'):
            media_type = 'photo'
            if hasattr(message, 'document') and message.document:
                file_size = getattr(message.document, 'size', 0)
        elif hasattr(message, 'video'):
            media_type = 'video'
            if hasattr(message, 'document') and message.document:
                file_size = getattr(message.document, 'size', 0)
        elif hasattr(message, 'document') and message.document:
            media_type = 'document'
            file_size = getattr(message.document, 'size', 0)
        else:
            return media_hashes

        if file_size > FILE_SIZE_LIMIT:
            return [{'type': media_type, 'skipped': True}]
            
        if media_type in ['photo', 'document']:
            try:
                file_bytes = await message.download_media(file=bytes)
                if not file_bytes:
                    return media_hashes
                    
                try:
                    # Generate multiple hashes for better detection
                    img = normalize_image(file_bytes)
                    phash = str(imagehash.phash(img))
                    dhash = str(imagehash.dhash(img))
                    ahash = str(imagehash.average_hash(img))
                    sha256 = hashlib.sha256(file_bytes).hexdigest()
                    
                    media_hashes.append({
                        'type': media_type,
                        'phash': phash,
                        'dhash': dhash,
                        'ahash': ahash,
                        'sha256': sha256
                    })
                except UnidentifiedImageError:
                    # For non-image documents, use SHA256 only
                    media_hashes.append({
                        'type': media_type,
                        'sha256': hashlib.sha256(file_bytes).hexdigest()
                    })
            except Exception as e:
                logger.error(f"Error processing {media_type}: {e}")

        elif media_type == 'video':
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                    tmp_path = tmp.name
                    await message.download_media(file=tmp_path)
                    
                    # Generate all hashes for videos
                    video_hashes = compute_video_hashes(tmp_path)
                    with open(tmp_path, 'rb') as f:
                        file_bytes = f.read()
                    sha256 = hashlib.sha256(file_bytes).hexdigest()
                    
                    if video_hashes:
                        media_hashes.append({
                            'type': 'video',
                            'phash': video_hashes.get('phash'),
                            'dhash': video_hashes.get('dhash'),
                            'ahash': video_hashes.get('ahash'),
                            'sha256': sha256
                        })
                    else:
                  
                        media_hashes.append({
                            'type': 'video',
                            'sha256': sha256
                        })
            except Exception as e:
                logger.error(f"Error processing video: {e}")
            finally:
                if 'tmp_path' in locals() and os.path.exists(tmp_path):
                    try:
                        os.remove(tmp_path)
                    except Exception as e:
                        logger.error(f"Error deleting temp file: {e}")
    
    except Exception as e:
        logger.error(f"Error in generate_media_hashes: {e}")
    
    return media_hashes