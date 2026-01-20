"""
Unit tests for entity extractor module.
"""
import pytest
from src.entity_extractor import EntityExtractor


class TestEntityExtractor:
    """Test cases for EntityExtractor class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.extractor = EntityExtractor(language='en')
        self.sample_articles = [
            {'title': 'Apple releases new iPhone in California'},
            {'title': 'Microsoft announces partnership with OpenAI'},
            {'title': 'Apple and Microsoft compete in tech market'},
            {'title': 'President Biden visits New York'}
        ]
    
    def test_extract_entities_basic(self):
        """Test basic entity extraction."""
        entities = self.extractor.extract_entities(self.sample_articles)
        
        # Should find some entities
        assert len(entities) > 0
        
        # Check that entities have correct format (entity, type, count)
        for entity, entity_type, count in entities:
            assert isinstance(entity, str)
            assert isinstance(entity_type, str)
            assert isinstance(count, int)
            assert count > 0
    
    def test_extract_entities_frequency(self):
        """Test that entities are sorted by frequency."""
        entities = self.extractor.extract_entities(self.sample_articles)
        
        if len(entities) > 1:
            # Check that frequencies are in descending order
            for i in range(len(entities) - 1):
                assert entities[i][2] >= entities[i + 1][2]
    
    def test_extract_entities_empty(self):
        """Test entity extraction with empty articles."""
        entities = self.extractor.extract_entities([])
        assert entities == []
    
    def test_format_entities_output(self):
        """Test entity output formatting."""
        entities = [
            ('Apple', 'ORG', 3),
            ('Microsoft', 'ORG', 2),
            ('Biden', 'PERSON', 1)
        ]
        
        output = self.extractor.format_entities_output(entities)
        
        assert 'Apple' in output
        assert 'Microsoft' in output
        assert 'Biden' in output
        assert 'ORG' in output
        assert 'PERSON' in output
    
    def test_format_entities_empty(self):
        """Test formatting empty entities list."""
        output = self.extractor.format_entities_output([])
        assert 'No named entities found' in output
