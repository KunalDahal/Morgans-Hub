import re
import logging
from typing import List, Optional
from util import load_remove_words, load_replace_words, escape_markdown_v2
from morgan_c.editor.detect_it import translate_text as translate_it
from morgan.edit.detect_ru import translate_text as translate_ru

logger = logging.getLogger(__name__)

class Editor:
    def __init__(self):
        self.remove_words = load_remove_words()
        self.replace_words = load_replace_words()
        self.max_chunk_length = 5000 
        logger.info(f"Loaded remove words: {self.remove_words}")
        logger.info(f"Loaded replace words: {self.replace_words}")
            
    def extract_links(self, text):
        """Extract all URLs from text"""
        if not text:
            return []
        url_pattern = re.compile(r'https?://\S+')
        return list(set(url_pattern.findall(text)))

    def replace_words_in_text(self, text):
        """Replace specified words in text"""
        if not text or not self.replace_words:
            return text
        for original, replacement in self.replace_words.items():
            pattern = re.compile(re.escape(original), re.IGNORECASE)
            text = pattern.sub(replacement, text)
        return text

    def remove_hashtags(self, text):
        """Remove all hashtags from text"""
        if not text:
            return text
        return re.sub(r'#\S+', '', text)

    def remove_emojis(self, text):
        """Remove all emojis from text"""
        if not text:
            return text
            
        emoji_pattern = re.compile(
            "["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F700-\U0001F77F"  # alchemical symbols
            u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
            u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
            u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
            u"\U0001FA00-\U0001FA6F"  # Chess Symbols
            u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
            u"\U00002702-\U000027B0"  # Dingbats
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
            
        return emoji_pattern.sub('', text)

    def split_text_into_chunks(self, text: str) -> List[str]:
        """Split text into chunks while preserving paragraphs"""
        if len(text) <= self.max_chunk_length:
            return [text]
            
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            if len(current_chunk) + len(para) > self.max_chunk_length:
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = ""
         
                if len(para) > self.max_chunk_length:
                    sentences = re.split(r'(?<=[.!?])\s+', para)
                    for sentence in sentences:
                        if len(current_chunk) + len(sentence) > self.max_chunk_length:
                            if current_chunk:
                                chunks.append(current_chunk)
                                current_chunk = ""
                        current_chunk += sentence + " "
                else:
                    current_chunk = para + "\n\n"
            else:
                current_chunk += para + "\n\n"
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
            
        return chunks

    def translate_text(self, text, lang: Optional[str] = None):
        """Translate text to English if language specified, while preserving newlines and structure"""
        try:
            if not text or not lang:
                return text
            
            special_chars = ""
            if text and text[0] in ('❖'):
                special_chars = text[0] + ' '
                text = text[1:].lstrip()
            
            logger.info(f"Text to translate ({lang}): '{text}'")
            
            paragraphs = text.split('\n')
            translated_paragraphs = []
            
            for para in paragraphs:
                if not para.strip():  
                    translated_paragraphs.append('')
                    continue
                    
                if len(para) > self.max_chunk_length:
                    chunks = self.split_text_into_chunks(para)
                    translated_chunks = []
                    for chunk in chunks:
                        translated = translate_it(chunk) if lang == 'it' else translate_ru(chunk)
                        translated_chunks.append(translated)
                    translated_para = ' '.join(translated_chunks)
                else:
                    translated_para = translate_it(para) if lang == 'it' else translate_ru(para)
                
                translated_paragraphs.append(translated_para)
            
            translated_text = '\n'.join(translated_paragraphs)
            translated_text = translated_text.strip()
            
            logger.info(f"Translation result: '{translated_text}'")
            
            return special_chars + translated_text
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            return special_chars + text
        
    def remove_words_from_text(self, text):
        """Remove specified words and phrases from text while preserving newlines"""
        if not text or not self.remove_words:
            return text
            
        logger.info(f"Original text: '{text}'")
        
        patterns = []
        for phrase in self.remove_words:
            phrase = phrase.strip()
            if not phrase:
                continue
                
            escaped = re.escape(phrase)
            pattern = escaped.replace(r'\ ', r'\s+')  
            patterns.append(pattern)
            
        if patterns:
            combined_pattern = re.compile('|'.join(patterns), re.IGNORECASE)
            
            cleaned_text = combined_pattern.sub('', text)
        else:
            cleaned_text = text

        cleaned_text = re.sub(r'[ \t]{2,}', ' ', cleaned_text)
        cleaned_text = '\n'.join(line.strip() for line in cleaned_text.split('\n'))
        cleaned_text = re.sub(r'\n\s*\n', '\n\n', cleaned_text)
        
        logger.info(f"Cleaned text: '{cleaned_text}'")
        return cleaned_text

    def remove_info_symbols(self, text):
        """Remove common info symbols like ℹ️ℹ️ℹ️"""
        if not text:
            return text
        info_pattern = re.compile(r'ℹ️+ℹ*️*\s*')
        return info_pattern.sub('', text)

    async def process(self, caption, translation_lang: Optional[str] = None):
        if caption is None:
            caption = ""
        logger.info(f"Initial caption: '{caption}'")
        
        # New STEP 0: Remove info symbols
        no_info = self.remove_info_symbols(caption)
        logger.info(f"After info symbol removal: '{no_info}'")
        
        # STEP 1: Remove unwanted phrases FIRST
        cleaned = self.remove_words_from_text(no_info)
        logger.info(f"After phrase removal: '{cleaned}'")
        
        # STEP 2: Remove hashtags
        no_hashtags = self.remove_hashtags(cleaned)
        logger.info(f"After hashtag removal: '{no_hashtags}'")
        
        # STEP 3: Remove URLs
        url_removed = re.sub(r'https?://\S+', '', no_hashtags)
        logger.info(f"After URL removal: '{url_removed}'")
        
        # STEP 4: Remove emojis
        no_emojis = self.remove_emojis(url_removed)
        logger.info(f"After emoji removal: '{no_emojis}'")
        
        # STEP 5: Translate if language specified
        if translation_lang: 
            translated = self.translate_text(no_emojis.strip(), translation_lang)
            logger.info(f"After translation: '{translated}'")
        else:
            translated = no_emojis.strip()
        
        # STEP 6: Replace words
        replaced = self.replace_words_in_text(translated)
        logger.info(f"After word replacement: '{replaced}'")
        
        header_line = "─── ⋆⋅☆⋅⋆ ───"
        footer_line = "─── ⋆⋅☆⋅⋆ ───"
        headerl = f"`{header_line.center(65)}`\n\n" 

        footer_text = escape_markdown_v2("💠 ~ @Animes_News_Ocean")
        footerl = f"\n\n`{footer_line.center(65)}`\n\n> _*{footer_text}*_" 

        main_text = escape_markdown_v2(replaced)
        main_text = f"❖ {main_text}" if main_text else ""
        formatted_text = f"*{main_text}*" if main_text else ""

        final_output = f"{headerl}{formatted_text}{footerl}"
        logger.info(f"Final output: '{final_output}'")
        return final_output