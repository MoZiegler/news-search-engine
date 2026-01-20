"""
Entity extractor module.
Handles Named Entity Recognition (NER) on news article headlines using spaCy.
"""
from typing import List, Dict, Tuple
from collections import Counter
import spacy
from src.i18n import t


class EntityExtractor:
    """Extracts and analyzes named entities from news article headlines."""
    
    def __init__(self, language: str = 'en'):
        """
        Initialize the entity extractor with a spaCy model.
        
        Args:
            language: Language code ('en' for English, 'de' for German)
        """
        self.language = language
        self.nlp = None
    
    def _load_model(self):
        """Load the appropriate spaCy model based on language."""
        if self.nlp is not None:
            return
        
        # Map language codes to spaCy models
        model_map = {
            'en': 'en_core_web_sm',
            'de': 'de_core_news_sm'
        }
        
        # Get model name for language, fallback to English if language not supported
        model_name = model_map.get(self.language, 'en_core_web_sm')
        
        print(t('ner.loading', model=model_name))
        try:
            self.nlp = spacy.load(model_name)
            print(t('ner.loaded'))
        except OSError:
            print(f"\n{t('ner.not_found', model=model_name)}")
            print(t('ner.download_instruction', model=model_name))
            print(f"{t('ner.fallback')}\n")
            self.nlp = None
    
    def extract_entities(self, articles: List[Dict]) -> List[Tuple[str, str, int]]:
        """
        Extract named entities from article headlines and sort by frequency.
        
        Args:
            articles: List of article dictionaries containing 'title' field
            
        Returns:
            List of tuples (entity_text, entity_type, frequency) sorted by frequency
        """
        if not articles:
            return []
        
        self._load_model()
        
        # Collect all entities
        all_entities = []
        
        if self.nlp:
            for article in articles:
                title = article.get('title', '')
                if title and title != 'N/A':
                    doc = self.nlp(title)
                    for ent in doc.ents:
                        # Filter out very short entities (likely noise)
                        if len(ent.text.strip()) > 1:
                            all_entities.append((ent.text.strip(), ent.label_))
        else:
            # Fallback: simple capitalized word extraction
            for article in articles:
                title = article.get('title', '')
                if title and title != 'N/A':
                    words = title.split()
                    for word in words:
                        # Simple heuristic: capitalized words might be entities
                        clean_word = word.strip('.,!?;:"\'-')
                        if (clean_word and 
                            clean_word[0].isupper() and 
                            len(clean_word) > 2 and
                            clean_word.lower() not in ['the', 'and', 'for', 'with', 'from']):
                            all_entities.append((clean_word, 'UNKNOWN'))
        
        # Count entity frequencies
        entity_counter = Counter(all_entities)
        
        # Sort by frequency (descending) and format results
        sorted_entities = [
            (entity, entity_type, count)
            for (entity, entity_type), count in entity_counter.most_common()
        ]
        
        return sorted_entities
    
    def format_entities_output(self, entities: List[Tuple[str, str, int]]) -> str:
        """
        Format the entities list for display.
        
        Args:
            entities: List of (entity, type, frequency) tuples
            
        Returns:
            Formatted string for display
        """
        if not entities:
            return t('ner.no_entities')
        
        output = f"\n{t('ner.header')}\n"
        output += "=" * 60 + "\n"
        output += f"{t('ner.entity'):<30} {t('ner.type'):<15} {t('ner.frequency'):<10}\n"
        output += "-" * 60 + "\n"
        
        for entity, entity_type, count in entities:
            # Truncate long entity names
            entity_display = entity[:28] + '..' if len(entity) > 30 else entity
            output += f"{entity_display:<30} {entity_type:<15} {count:<10}\n"
        
        return output
