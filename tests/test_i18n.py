"""
Unit tests for i18n (internationalization) module.
"""
import os
import json
from pathlib import Path
from src.i18n import Translator, set_language, t


class TestTranslator:
    """Test cases for Translator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.translator = Translator()
    
    def test_translator_initialization(self):
        """Test translator initializes with default language."""
        assert self.translator.current_language == 'en'
        assert 'en' in self.translator.translations
        assert 'de' in self.translator.translations
    
    def test_set_language_english(self):
        """Test setting language to English."""
        self.translator.set_language('en')
        assert self.translator.current_language == 'en'
    
    def test_set_language_german(self):
        """Test setting language to German."""
        self.translator.set_language('de')
        assert self.translator.current_language == 'de'
    
    def test_set_language_unsupported_fallback(self):
        """Test unsupported language falls back to English."""
        self.translator.set_language('fr')  # French not supported
        assert self.translator.current_language == 'en'
    
    def test_translate_simple_key_english(self):
        """Test simple translation in English."""
        self.translator.set_language('en')
        result = self.translator.t('app.title')
        assert result == 'News Search Engine'
    
    def test_translate_simple_key_german(self):
        """Test simple translation in German."""
        self.translator.set_language('de')
        result = self.translator.t('app.title')
        assert result == 'Nachrichten-Suchmaschine'
    
    def test_translate_nested_key(self):
        """Test translation with nested keys (dot notation)."""
        self.translator.set_language('en')
        result = self.translator.t('search.prompt')
        assert 'topic' in result.lower()
    
    def test_translate_with_format_arguments(self):
        """Test translation with string formatting."""
        self.translator.set_language('en')
        result = self.translator.t('search.found', count=5)
        assert '5' in result
        assert 'articles' in result.lower()
    
    def test_translate_missing_key_returns_key(self):
        """Test that missing translation key returns the key itself."""
        result = self.translator.t('nonexistent.key')
        assert result == 'nonexistent.key'
    
    def test_translate_invalid_format_args(self):
        """Test translation handles invalid format arguments gracefully."""
        self.translator.set_language('en')
        # Try to format with wrong arguments
        result = self.translator.t('search.found', wrong_arg='value')
        # Should return the string, possibly unformatted
        assert isinstance(result, str)
    
    def test_global_set_language_function(self):
        """Test global set_language function."""
        set_language('de')
        result = t('app.title')
        assert result == 'Nachrichten-Suchmaschine'
        
        # Reset to English
        set_language('en')
    
    def test_global_t_function(self):
        """Test global t (translate) function."""
        set_language('en')
        result = t('app.welcome')
        assert 'Welcome' in result
    
    def test_translation_files_exist(self):
        """Test that translation files exist and are valid JSON."""
        translations_dir = Path(__file__).parent.parent / 'translations'
        
        # Check English translation file
        en_file = translations_dir / 'en.json'
        assert en_file.exists()
        with open(en_file, 'r', encoding='utf-8') as f:
            en_data = json.load(f)
            assert isinstance(en_data, dict)
            assert 'app' in en_data
        
        # Check German translation file
        de_file = translations_dir / 'de.json'
        assert de_file.exists()
        with open(de_file, 'r', encoding='utf-8') as f:
            de_data = json.load(f)
            assert isinstance(de_data, dict)
            assert 'app' in de_data
    
    def test_translation_completeness(self):
        """Test that German translations have same keys as English."""
        en_keys = self._get_all_keys(self.translator.translations['en'])
        de_keys = self._get_all_keys(self.translator.translations['de'])
        
        # German should have all English keys (allowing for extras)
        missing_keys = en_keys - de_keys
        assert len(missing_keys) == 0, f"Missing German translations for: {missing_keys}"
    
    def _get_all_keys(self, d, parent_key=''):
        """Helper to get all nested keys from translation dictionary."""
        keys = set()
        for k, v in d.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, dict):
                keys.update(self._get_all_keys(v, new_key))
            else:
                keys.add(new_key)
        return keys
