"""
Unit tests for summarizer module.
"""
import pytest
from src.summarizer import Summarizer


class TestSummarizer:
    """Test cases for Summarizer class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.summarizer = Summarizer()
        self.sample_articles = [
            {'title': 'Tech companies announce new AI products'},
            {'title': 'Stock market reaches new highs amid economic growth'},
            {'title': 'Climate change summit brings world leaders together'}
        ]
    
    def test_summarize_headlines_basic(self):
        """Test basic headline summarization."""
        summary = self.summarizer.summarize_headlines(self.sample_articles)
        
        assert summary is not None
        assert isinstance(summary, str)
        assert len(summary) > 0
    
    def test_summarize_empty_articles(self):
        """Test summarization with empty articles list."""
        summary = self.summarizer.summarize_headlines([])
        assert summary == "No articles to summarize."
    
    def test_summarize_no_titles(self):
        """Test summarization with articles without titles."""
        articles = [{'url': 'https://example.com'}]
        summary = self.summarizer.summarize_headlines(articles)
        assert 'No valid headlines' in summary or 'Combined Headlines' in summary
    
    def test_fallback_summary(self):
        """Test fallback summary method."""
        headlines = [
            'First headline about technology',
            'Second headline about politics',
            'Third headline about sports'
        ]
        
        summary = self.summarizer._fallback_summary(headlines)
        
        assert 'First headline' in summary
        assert 'Second headline' in summary
        assert 'Third headline' in summary
