import os
from typing import List,Union,Dict,Any
import json
from dotenv import load_dotenv
load_dotenv()
import re

import logging

logger = logging.getLogger(__name__)

JSON_FOLDER = "JSON"
os.makedirs(JSON_FOLDER, exist_ok=True)

REQ_FILE = os.path.join(JSON_FOLDER, "requests.json")
USER_FILE = os.path.join(JSON_FOLDER, "users.json")
REPLACE_FILE = os.path.join(JSON_FOLDER, "replace.json")
REMOVE_FILE = os.path.join(JSON_FOLDER, "remove.json")
SOURCE_FILE = os.path.join(JSON_FOLDER, "source_id.json")
HASH_FILE = os.path.join(JSON_FOLDER, "hash.json")
BAN_FILE = os.path.join(JSON_FOLDER, "banned_words.json")
RECOVERY_FILE = os.path.join(JSON_FOLDER, "last_message_id.json")
UPVOTE_FILE=os.path.join(JSON_FOLDER,"upvote.json")
TARGET_FILE=os.path.join(JSON_FOLDER,"target_id.json")

MAX_HASH_ENTRIES = int(os.getenv('MAX_HASH_ENTRIES', 10000))
FILE_SIZE_LIMIT =  2_000_000_000  # 2GB

for file in [
    SOURCE_FILE,USER_FILE,TARGET_FILE, REMOVE_FILE,BAN_FILE
]:
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump([], f)

for file in [HASH_FILE,RECOVERY_FILE,REQ_FILE, REPLACE_FILE,UPVOTE_FILE]:
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump({}, f)


def format_text(text):
    """Convert text to the requested font style"""
    font_map = {
        'a': '𝗮', 'b': '𝗯', 'c': '𝗰', 'd': '𝗱', 'e': '𝗲', 'f': '𝗳', 'g': '𝗴',
        'h': '𝗵', 'i': '𝗶', 'j': '𝗷', 'k': '𝗸', 'l': '𝗹', 'm': '𝗺', 'n': '𝗻',
        'o': '𝗼', 'p': '𝗽', 'q': '𝗾', 'r': '𝗿', 's': '𝘀', 't': '𝘁', 'u': '𝘂',
        'v': '𝘃', 'w': '𝘄', 'x': '𝘅', 'y': '𝘆', 'z': '𝘇',
        'A': '𝗔', 'B': '𝗕', 'C': '𝗖', 'D': '𝗗', 'E': '𝗘', 'F': '𝗙', 'G': '𝗚',
        'H': '𝗛', 'I': '𝗜', 'J': '𝗝', 'K': '𝗞', 'L': '𝗟', 'M': '𝗠', 'N': '𝗡',
        'O': '𝗢', 'P': '𝗣', 'Q': '𝗤', 'R': '𝗥', 'S': '𝗦', 'T': '𝗧', 'U': '𝗨',
        'V': '𝗩', 'W': '𝗪', 'X': '𝗫', 'Y': '𝗬', 'Z': '𝗭',
        ' ': ' ', '!': '!', '?': '?', '.': '.', ',': ',', ':': ':', ';': ';',
        '0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰', '5': '𝟱', '6': '𝟲',
        '7': '𝟳', '8': '𝟴', '9': '𝟵', '@': '@'
    }
    return ''.join(font_map.get(c, c) for c in text)

def get_api_id():
    return int(os.getenv("API_ID"))

def get_api_hash():
    return os.getenv("API_HASH")

def get_session_string():
    session = os.getenv("SESSION_STRING")
    if not session:
        raise ValueError("SESSION_STRING not found in .env file")
    return session

def get_bot_token_2():
    token = os.getenv("BOT_TOKEN_2")
    if not token:
        raise ValueError("BOT_TOKEN not found in .env file")
    return token

def get_admin_ids():
    """Get list of admin user IDs from environment"""
    admin_ids = os.getenv('ADMIN_IDS', '').split(',')
    return [int(id.strip()) for id in admin_ids if id.strip().isdigit()]

def get_bot_token():
    token = os.getenv("BOT_TOKEN_1")
    if not token:
        raise ValueError("BOT_TOKEN_1 not found in .env file")
    return token


def escape_markdown_v2(text: str) -> str:
    if not text:
        return ""
    
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    
    lines = text.split('\n')
    escaped_lines = []
    
    for line in lines:
        pattern = f'([{"".join(re.escape(c) for c in escape_chars)}])'
        escaped_line = re.sub(pattern, r'\\\1', line)
        escaped_lines.append(escaped_line)
    
    return '\n'.join(escaped_lines)


def load_replace_words():
    """Load word replacements from JSON file"""
    try:
        if not os.path.exists(REPLACE_FILE):
            return {}

        with open(REPLACE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading replace words: {e}")
        return {}


def load_remove_words() -> List[str]:
    try:
        os.makedirs(JSON_FOLDER, exist_ok=True)

        if not os.path.exists(REMOVE_FILE):
            return []

        with open(REMOVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [word.strip() for word in data if word.strip()]  # Simplified loading

    except Exception as e:
        logger.error(f"Error loading {REMOVE_FILE}: {e}")
        return []

def get_target_id():
    return os.getenv("ANO_ID")

def get_target_channel() -> List[int]:
    """Get target channel ID from environment"""
    channel_id = get_target_id()
    if not channel_id:
        raise ValueError("ANO_ID not found in .env file")
    return [int(channel_id)]

def get_vid_channel_id() -> int:

    channel_id = os.getenv("VID_CHANNEL_ID")
    if not channel_id:
        raise ValueError("VID_CHANNEL_ID not found in .env file")
    return int(channel_id)
            
def load_banned_words():
    with open(BAN_FILE, "r") as f:
        return json.load(f)

def save_banned_words(words):
    with open(BAN_FILE, "w") as f:
        json.dump(words, f)


def save_remove_words(words):
    os.makedirs(JSON_FOLDER, exist_ok=True)
    with open(REMOVE_FILE, "w") as f:
        json.dump(words, f, indent=2)


def save_replace_words(replace_dict):
    """Save word replacements to JSON file"""
    try:
        os.makedirs(JSON_FOLDER, exist_ok=True)
        with open(REPLACE_FILE, "w", encoding="utf-8") as f:
            json.dump(replace_dict, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving replace words: {e}")
        return False

def load_channels():
    if not os.path.exists(SOURCE_FILE):
        return []
    with open(SOURCE_FILE, "r") as f:
        data = json.load(f)
    return [int(cid) for cid in data]


def save_channels(channel_list):
    os.makedirs(JSON_FOLDER, exist_ok=True)
    with open(SOURCE_FILE, "w") as f:
        json.dump(channel_list, f, indent=2)


def load_users() -> List[str]:
    try:

        os.makedirs(JSON_FOLDER, exist_ok=True)

        # Return empty list if file doesn't exist
        if not os.path.exists(USER_FILE):
            return []

        # Load and validate existing data
        with open(USER_FILE, "r") as f:
            users = json.load(f)

            # Ensure we always return a list of strings
            if not isinstance(users, list):
                raise ValueError("Invalid data format in user.json")

            return [str(user_id) for user_id in users]

    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error loading user data: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error loading users: {e}")
        return []


def save_users(user_ids: List[Union[str, int]]) -> bool:
    try:
        # Convert all IDs to strings and remove duplicates
        unique_users = list({str(uid) for uid in user_ids})

        # Create directory if it doesn't exist
        os.makedirs(JSON_FOLDER, exist_ok=True)

        # Write to file with pretty formatting
        with open(USER_FILE, "w") as f:
            json.dump(unique_users, f, indent=2, ensure_ascii=False)

        return True
    except Exception as e:
        print(f"Error saving user data: {e}")
        return False


def add_user(user_id: Union[str, int]) -> bool:

    try:
        users = load_users()
        user_str = str(user_id)

        if user_str not in users:
            users.append(user_str)
            return save_users(users)
        return True  # Already exists
    except Exception as e:
        print(f"Error adding user: {e}")
        return False

def load_upvotes() -> Dict[str, Any]:
    """Load upvote data from JSON file"""
    try:
        os.makedirs(JSON_FOLDER, exist_ok=True)
        if not os.path.exists(UPVOTE_FILE):
            return {"count": 0, "users": {}}
        
        with open(UPVOTE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "users" not in data:
                data["users"] = {}
            if "count" not in data:
                data["count"] = 0
            return data
    except Exception as e:
        print(f"Error loading upvote data: {e}")
        return {"count": 0, "users": {}}
    
def save_upvotes(data: Dict[str, Any]) -> bool:
    """Save upvote data to JSON file"""
    try:
        with open(UPVOTE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving upvote data: {e}")
        return False

def get_bot_username():
    username = os.getenv("BOT_USERNAME")
    if not username:
        raise ValueError("BOT_USERNAME not found in .env file")
    return username.lstrip("@")
        
