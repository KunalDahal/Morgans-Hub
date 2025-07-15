# hash.py
import hashlib
import os
import json
import logging
import tempfile
from PIL import Image,UnidentifiedImageError
import imagehash
import io
from moviepy import VideoFileClip
from typing import List, Dict
from util import HASH_FILE, FILE_SIZE_LIMIT

logger = logging.getLogger(__name__)

def compute_video_hashes(video_path: str) -> Dict[str, str]:
    try:
        clip = VideoFileClip(video_path)
        end_time = min(10, clip.duration)

        md5_hash = hashlib.md5()
        sha256_hash = hashlib.sha256()

        for t, img in clip.iter_frames(fps=2, with_times=True):
            if t > end_time:
                break
            frame_bytes = img.tobytes()
            md5_hash.update(frame_bytes)
            sha256_hash.update(frame_bytes)

        clip.close()
        return {
            'md5': md5_hash.hexdigest(),
            'sha256': sha256_hash.hexdigest()
        }
    except Exception as e:
        logger.error(f"Error computing video hashes: {e}")
        return {'md5': '', 'sha256': ''}

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

# hash.py
async def generate_media_hashes(message) -> List[Dict]:
    media_hashes = []
    
    if not hasattr(message, 'media') or not message.media:
        return media_hashes

    try:
        # Get the media type first
        media_type = None
        file_size = 0
        
        # Determine media type and size more safely
        if hasattr(message, 'photo'):
            media_type = 'photo'
            # Check for document attribute safely
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
            # Unsupported media type
            return media_hashes

        # Skip if over size limit (only if we could determine size)
        if file_size > FILE_SIZE_LIMIT:
            return [{'type': media_type, 'skipped': True}]
        if media_type == 'photo':
            try:
                file_bytes = await message.download_media(file=bytes)
                if not file_bytes:
                    return media_hashes
                    
                try:
                    image = Image.open(io.BytesIO(file_bytes))
                    media_hashes.append({
                        'type': 'photo',
                        'sha256': hashlib.sha256(file_bytes).hexdigest(),
                    })
                except UnidentifiedImageError:
                    logger.warning("Could not identify image file, using SHA256 only")
                    media_hashes.append({
                        'type': 'photo',
                        'sha256': hashlib.sha256(file_bytes).hexdigest(),
                    })
            except Exception as e:
                logger.error(f"Error processing photo: {e}")

        elif media_type == 'video':
            try:
                with tempfile.NamedTemporaryFile(delete=False) as tmp:
                    tmp_path = tmp.name
                    await message.download_media(file=tmp_path)
                    hashes = compute_video_hashes(tmp_path)
                    media_hashes.append({
                        'type': 'video',
                        'sha256': hashes['sha256'],
                    })
            except Exception as e:
                logger.error(f"Error processing video: {e}")
            finally:
                if 'tmp_path' in locals() and os.path.exists(tmp_path):
                    os.remove(tmp_path)

        elif media_type == 'document':
            try:
                file_bytes = await message.download_media(file=bytes)
                media_hashes.append({
                    'type': 'document',
                    'sha256': hashlib.sha256(file_bytes).hexdigest(),
                })
            except Exception as e:
                logger.error(f"Error processing document: {e}")
    
    except Exception as e:
        logger.error(f"Error in generate_media_hashes: {e}")
    
    return media_hashes