"""
Environment-based internationalization (i18n) module for the News Search Engine.
Handles translation of UI strings based on selected language.

For larger projects, consider using Python's built-in gettext with .po files, but the JSON approach is simpler and more than sufficient for this use case.
"""
import json
from pathlib import Path
from typing import Dict


class Translator:
    """Simple translation handler for multi-language support."""
    
    def __init__(self):
        """Initialize translator with default language."""
        self.current_language = 'en'
        self.translations = {}
        self._load_translations()
    
    def _load_translations(self):
        """Load translation files for all supported languages."""
        translations_dir = Path(__file__).parent.parent / 'translations'
        
        for lang_file in translations_dir.glob('*.json'):
            lang_code = lang_file.stem
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    self.translations[lang_code] = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load translations for {lang_code}: {e}")
    
    def set_language(self, language: str):
        """
        Set the current language for translations.
        
        Args:
            language: Language code ('en' or 'de')
        """
        if language in self.translations:
            self.current_language = language
        else:
            print(f"Warning: Language '{language}' not supported, using English")
            self.current_language = 'en'
    
    def t(self, key: str, **kwargs) -> str:
        """
        Translate a key to the current language.
        
        Args:
            key: Translation key (dot-notation supported, e.g., 'search.prompt')
            **kwargs: Format arguments for string interpolation
            
        Returns:
            Translated string
        """
        # Get translation for current language, fallback to English
        lang_dict = self.translations.get(self.current_language, self.translations.get('en', {}))
        
        # Support nested keys with dot notation
        keys = key.split('.')
        value = lang_dict
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, key)
            else:
                value = key
                break
        
        # Apply string formatting if kwargs provided
        if kwargs and isinstance(value, str):
            try:
                value = value.format(**kwargs)
            except KeyError:
                pass
        
        return value if isinstance(value, str) else key


# Global translator instance
_translator = Translator()


def set_language(language: str):
    """Set the application language."""
    _translator.set_language(language)


def t(key: str, **kwargs) -> str:
    """Shorthand for translation."""
    return _translator.t(key, **kwargs)
