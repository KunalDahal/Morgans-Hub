import re
import logging
from deep_translator import GoogleTranslator
from util import load_remove_words, load_replace_words, escape_markdown_v2
from summa import summarizer

logger = logging.getLogger(__name__)

class Editor:
    def __init__(self):
        self.remove_words = load_remove_words()
        self.replace_words = load_replace_words()
        logger.info(f"Loaded remove words: {self.remove_words}")
        logger.info(f"Loaded replace words: {self.replace_words}")
            
    def extract_links(self, text):
        """Extract all URLs from text"""
        if not text:
            return []
        url_pattern = re.compile(r'https?://\S+')
        return list(set(url_pattern.findall(text)))

    def summarize_text(self, text):
        """Summarize text while preserving paragraph structure"""
        if not text:
            return text
            
        # Split into paragraphs first
        paragraphs = text.split('\n\n')
        
        # Process each paragraph separately
        processed_paragraphs = []
        for para in paragraphs:
            # Skip empty paragraphs
            if not para.strip():
                continue
                
            word_count = len(para.split())
            if word_count <= 151:
                processed_paragraphs.append(para)
                continue
                
            summary = summarizer.summarize(para, words=200)
            if not summary:
                processed_paragraphs.append(para)
                continue

            sentences = re.split(r'(?<=[.!?])\s+', summary)
            sentences = [s.strip() for s in sentences if s.strip()]

            current_para = []
            current_words = 0

            for sentence in sentences:
                sentence_words = len(sentence.split())
                if current_words + sentence_words > 20:
                    processed_paragraphs.append(' '.join(current_para))
                    current_para = []
                    current_words = 0
                current_para.append(sentence)
                current_words += sentence_words

            if current_para:
                processed_paragraphs.append(' '.join(current_para))

        # Join paragraphs with double newlines
        return '\n\n'.join(processed_paragraphs)

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

    def translate_text(self, text):
        """Translate text to English while preserving structure and special characters"""
        try:
            if not text:
                return ""
            
            # Preserve special prefix characters
            special_chars = ""
            if text and text[0] in ('❄️'):
                special_chars = text[0] + ' '
                text = text[1:].lstrip()
            
            # Add debug logging
            logger.info(f"Text to translate: '{text}'")
            
            # Try with explicit Italian source first, then fallback to auto
            translated = GoogleTranslator(source='it', target='en').translate(text)
            if not translated:
                translated = GoogleTranslator(source='auto', target='en').translate(text)
                
            # Add debug logging
            logger.info(f"Translation result: '{translated}'")
            
            # Handle translation failures
            if not translated:
                return special_chars + text
            
            # Reattach special characters
            return special_chars + translated
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            return special_chars + text
        
    def remove_words_from_text(self, text):
        """Remove specified words and phrases from text while preserving newlines"""
        if not text or not self.remove_words:
            return text
            
        logger.info(f"Original text: '{text}'")
        
        # Create patterns that match phrases with any whitespace variations
        patterns = []
        for phrase in self.remove_words:
            phrase = phrase.strip()
            if not phrase:
                continue
                
            # Create a flexible pattern that handles any whitespace
            escaped = re.escape(phrase)
            pattern = escaped.replace(r'\ ', r'\s+')  # Match any whitespace sequence
            patterns.append(pattern)
            
        # Combine patterns into one regex
        if patterns:
            combined_pattern = re.compile('|'.join(patterns), re.IGNORECASE)
            
            # Remove all matches
            cleaned_text = combined_pattern.sub('', text)
        else:
            cleaned_text = text
        
        # PRESERVE NEWLINES: Only clean extra spaces, not newlines
        # Compress consecutive spaces/tabs within lines
        cleaned_text = re.sub(r'[ \t]{2,}', ' ', cleaned_text)
        # Remove leading/trailing whitespace from each line
        cleaned_text = '\n'.join(line.strip() for line in cleaned_text.split('\n'))
        # Remove empty lines with whitespace
        cleaned_text = re.sub(r'\n\s*\n', '\n\n', cleaned_text)
        
        logger.info(f"Cleaned text: '{cleaned_text}'")
        return cleaned_text

    async def process(self, caption):
        if caption is None:
            caption = ""
        logger.info(f"Initial caption: '{caption}'")

        # STEP 1: Remove unwanted phrases FIRST
        cleaned = self.remove_words_from_text(caption)
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
        
        # STEP 5: Translate
        translated = self.translate_text(no_emojis.strip())
        logger.info(f"After translation: '{translated}'")
        
        # STEP 6: Replace words
        replaced = self.replace_words_in_text(translated)
        logger.info(f"After word replacement: '{replaced}'")
        
        # STEP 7: Summarize
        # summarized = self.summarize_text(replaced)
        # logger.info(f"After summarization: '{summarized}'")
        
        # Formatting
        main_text = escape_markdown_v2(replaced)
        footer_text = escape_markdown_v2("💠 ~ @Animes_News_Ocean")

        header = "_*@MorgansNews\_Bot*_"
        header_new = f"> ||{header}||\n\n"
        main_text = f"❄️ {main_text}" if main_text else ""
        formatted_text = f"*{main_text}*" if main_text else ""
        footer = f"\n\n> _*{footer_text}*_"

        final_output = f"{header_new}{formatted_text}{footer}"
        logger.info(f"Final output: '{final_output}'")
        return final_output