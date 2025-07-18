# check.py
from typing import Dict
import logging
from typing import List
from util import BAN_FILE, MAX_HASH_ENTRIES
from monitor.hash.hash import _load_hash_data, generate_media_hashes, _save_hash_data
import time
import os
import json

logger = logging.getLogger(__name__)

class ContentChecker:
    def __init__(self):
        self.banned_words = self._load_banned_words()
    
    def _load_banned_words(self) -> List[str]:
        try:
            if os.path.exists(BAN_FILE):
                with open(BAN_FILE, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error loading banned words: {e}")
            return []
    
    def _contains_banned_words(self, text: str) -> bool:
        if not text or not self.banned_words:
            return False
        text_lower = text.lower()
        return any(word in text_lower for word in self.banned_words)

    async def check_group_content(self, messages: List) -> Dict:
        if not messages:
            return {'clean_messages': [], 'has_banned': False, 'original_caption': ''}
        
        combined_caption = "\n".join(
            msg.message for msg in messages 
            if hasattr(msg, 'message') and msg.message
        )
        
        has_banned = self._contains_banned_words(combined_caption)
        
        clean_messages = []
        new_hashes = []
        hash_data = _load_hash_data()
        
        # Check duplicates for each message in the group
        for message in messages:
            media_list = await generate_media_hashes(message)
            is_duplicate = False
            
            for media in media_list:
                if media.get('skipped'):
                    continue
                    
                # Prefer phash if available, fall back to sha256
                media_key = media.get('phash') or media.get('sha256')
                
                if media_key and media_key in hash_data:
                    is_duplicate = True
                    break
                    
            # Only add non-duplicate messages
            if not is_duplicate:
                clean_messages.append(message)
                new_hashes.extend(media_list)
        
        # Update hash data only for new non-duplicate media
        if new_hashes:
            self._update_hash_data(new_hashes)
        
        return {
            'clean_messages': clean_messages,
            'has_banned': has_banned,
            'original_caption': combined_caption
        }

    async def check_content(self, message) -> int:
        if isinstance(message, list):
            result = await self.check_group_content(message)
            if len(result['clean_messages']) < len(message):
                return 1
            return 0
        
        media_list = await generate_media_hashes(message)
        hash_data = _load_hash_data()
        
        is_duplicate = any(
            (media.get('phash') or media.get('sha256')) in hash_data
            for media in media_list
            if not media.get('skipped')
        )
        
        if not is_duplicate and media_list:
            self._update_hash_data(media_list)
        
        return 1 if is_duplicate else 0
    
    def _update_hash_data(self, new_hashes: List[Dict]):
        try:
            current_data = _load_hash_data()
            
            for media in new_hashes:
                # Store both phash and sha256 if available, but prefer phash for lookup
                media_key = media.get('phash') or media.get('sha256')
                if media_key:
                    current_data[media_key] = {
                        'type': media.get('type'),
                        'timestamp': time.time(),
                        'phash': media.get('phash'),
                        'sha256': media.get('sha256')
                    }
            
            if len(current_data) > MAX_HASH_ENTRIES:
                sorted_items = sorted(current_data.items(), 
                                   key=lambda x: x[1].get('timestamp', 0))
                current_data = dict(sorted_items[-MAX_HASH_ENTRIES:])
            
            _save_hash_data(current_data)
            
        except Exception as e:
            logger.error(f"Error updating hash data: {e}")