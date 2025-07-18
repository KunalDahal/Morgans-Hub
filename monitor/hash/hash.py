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

def compute_video_phash(video_path: str) -> str:
    """Compute perceptual hash for a video by sampling frames"""
    try:
        clip = VideoFileClip(video_path)
        end_time = min(10, clip.duration)  # Use first 10 seconds or full video if shorter
        hashes = []
        
        # Sample frames at 2fps
        for t, img in clip.iter_frames(fps=2, with_times=True):
            if t > end_time:
                break
            try:
                pil_img = Image.fromarray(img)
                phash = str(imagehash.phash(pil_img))
                hashes.append(phash)
            except Exception as e:
                logger.error(f"Error processing video frame: {e}")
                continue
        
        clip.close()
        
        if not hashes:
            return ''
            
        # Combine frame hashes into one video hash
        return str(imagehash.average_hash([imagehash.hex_to_hash(h) for h in hashes]))
    except Exception as e:
        logger.error(f"Error computing video phash: {e}")
        return ''

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
                    # Generate pHash for images
                    img = Image.open(io.BytesIO(file_bytes))
                    phash = str(imagehash.phash(img))
                    sha256 = hashlib.sha256(file_bytes).hexdigest()
                    
                    media_hashes.append({
                        'type': media_type,
                        'phash': phash,
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
                    
                    # Generate both pHash and SHA256 for videos
                    phash = compute_video_phash(tmp_path)
                    with open(tmp_path, 'rb') as f:
                        file_bytes = f.read()
                    sha256 = hashlib.sha256(file_bytes).hexdigest()
                    
                    if phash:
                        media_hashes.append({
                            'type': 'video',
                            'phash': phash,
                            'sha256': sha256
                        })
                    else:
                        # Fallback to SHA256 if pHash fails
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