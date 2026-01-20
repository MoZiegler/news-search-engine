"""
Unit tests for news API client module.
"""
import os
from unittest.mock import patch, Mock
from src.news_api import NewsAPIClient


class TestNewsAPIClient:
    """Test cases for NewsAPIClient class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Mock the API key to avoid requiring real one
        with patch.dict(os.environ, {'NEWSAPI_KEY': 'test_api_key_12345'}):
            self.client = NewsAPIClient()
    
    @patch('src.news_api.NewsApiClient')
    def test_initialization_with_api_key(self, mock_newsapi):
        """Test NewsAPIClient initializes with API key from environment."""
        with patch.dict(os.environ, {'NEWSAPI_KEY': 'test_key'}):
            client = NewsAPIClient()
            mock_newsapi.assert_called_once_with(api_key='test_key')
    
    @patch('src.news_api.load_dotenv')  # Mock load_dotenv to prevent reading .env file
    def test_initialization_without_api_key_raises_error(self, mock_load_dotenv):
        """Test NewsAPIClient raises ValueError when API key is missing."""
        with patch.dict(os.environ, {}, clear=True):
            try:
                client = NewsAPIClient()
                assert False, "Should have raised ValueError"
            except ValueError as e:
                assert 'NEWSAPI_KEY' in str(e)
    
    @patch('src.news_api.NewsApiClient')
    def test_search_news_success(self, mock_newsapi):
        """Test successful news search."""
        # Arrange - Mock API response
        mock_instance = Mock()
        mock_instance.get_everything.return_value = {
            'status': 'ok',
            'totalResults': 2,
            'articles': [
                {
                    'title': 'Test Article 1',
                    'url': 'https://example.com/1',
                    'publishedAt': '2026-01-15T10:00:00Z',
                    'source': {'name': 'Test Source'},
                    'author': 'Test Author',
                    'description': 'Test description'
                },
                {
                    'title': 'Test Article 2',
                    'url': 'https://example.com/2',
                    'publishedAt': '2026-01-16T12:00:00Z',
                    'source': {'name': 'Another Source'},
                    'author': 'Another Author',
                    'description': 'Another description'
                }
            ]
        }
        mock_newsapi.return_value = mock_instance
        
        # Act
        with patch.dict(os.environ, {'NEWSAPI_KEY': 'test_key'}):
            client = NewsAPIClient()
            results = client.search_news('artificial intelligence', language='en')
        
        # Assert
        assert len(results) == 2
        assert results[0]['title'] == 'Test Article 1'
        assert results[1]['title'] == 'Test Article 2'
        
        # Verify API was called correctly
        mock_instance.get_everything.assert_called_once()
        call_kwargs = mock_instance.get_everything.call_args[1]
        assert call_kwargs['q'] == 'artificial intelligence'
        assert call_kwargs['language'] == 'en'
        assert call_kwargs['sort_by'] == 'relevancy'
    
    @patch('src.news_api.NewsApiClient')
    def test_search_news_german_language(self, mock_newsapi):
        """Test news search with German language."""
        mock_instance = Mock()
        mock_instance.get_everything.return_value = {
            'status': 'ok',
            'totalResults': 1,
            'articles': [
                {
                    'title': 'Deutsche Nachrichten',
                    'url': 'https://example.de/1',
                    'publishedAt': '2026-01-15T10:00:00Z',
                    'source': {'name': 'Test Quelle'},
                    'author': 'Test Autor',
                    'description': 'Test Beschreibung'
                }
            ]
        }
        mock_newsapi.return_value = mock_instance
        
        with patch.dict(os.environ, {'NEWSAPI_KEY': 'test_key'}):
            client = NewsAPIClient()
            results = client.search_news('künstliche intelligenz', language='de')
        
        assert len(results) == 1
        call_kwargs = mock_instance.get_everything.call_args[1]
        assert call_kwargs['language'] == 'de'
    
    @patch('src.news_api.NewsApiClient')
    def test_search_news_empty_results(self, mock_newsapi):
        """Test news search with no results."""
        mock_instance = Mock()
        mock_instance.get_everything.return_value = {
            'status': 'ok',
            'totalResults': 0,
            'articles': []
        }
        mock_newsapi.return_value = mock_instance
        
        with patch.dict(os.environ, {'NEWSAPI_KEY': 'test_key'}):
            client = NewsAPIClient()
            results = client.search_news('nonexistent topic')
        
        assert results == []
    
    @patch('src.news_api.NewsApiClient')
    def test_search_news_api_error(self, mock_newsapi):
        """Test news search handles API errors gracefully."""
        mock_instance = Mock()
        mock_instance.get_everything.side_effect = Exception('API Error')
        mock_newsapi.return_value = mock_instance
        
        with patch.dict(os.environ, {'NEWSAPI_KEY': 'test_key'}):
            client = NewsAPIClient()
            results = client.search_news('test query')
        
        # Should return empty list on error
        assert results == []
    
    @patch('src.news_api.NewsApiClient')
    def test_search_news_invalid_response(self, mock_newsapi):
        """Test news search handles invalid API response."""
        mock_instance = Mock()
        mock_instance.get_everything.return_value = {
            'status': 'error',
            'message': 'Invalid API key'
        }
        mock_newsapi.return_value = mock_instance
        
        with patch.dict(os.environ, {'NEWSAPI_KEY': 'test_key'}):
            client = NewsAPIClient()
            results = client.search_news('test query')
        
        assert results == []
    
    def test_format_published_date(self):
        """Test date formatting."""
        with patch.dict(os.environ, {'NEWSAPI_KEY': 'test_key'}):
            client = NewsAPIClient()
            
            # Test ISO format
            formatted = client.format_published_date('2026-01-15T10:30:00Z')
            assert '2026' in formatted
            assert '01' in formatted or 'Jan' in formatted
            assert '15' in formatted
    
    def test_format_published_date_invalid(self):
        """Test date formatting with invalid date string."""
        with patch.dict(os.environ, {'NEWSAPI_KEY': 'test_key'}):
            client = NewsAPIClient()
            
            # Invalid date should be returned as-is
            invalid_date = 'not-a-date'
            formatted = client.format_published_date(invalid_date)
            assert formatted == invalid_date
    
    @patch('src.news_api.NewsApiClient')
    def test_article_transformation(self, mock_newsapi):
        """Test article data transformation/normalization."""
        mock_instance = Mock()
        mock_instance.get_everything.return_value = {
            'status': 'ok',
            'articles': [
                {
                    'title': 'Test',
                    'url': 'http://test.com',
                    'publishedAt': '2026-01-15T10:00:00Z',
                    'source': {'name': 'Source'},
                    'author': 'Author',
                    'description': 'Desc'
                }
            ]
        }
        mock_newsapi.return_value = mock_instance
        
        with patch.dict(os.environ, {'NEWSAPI_KEY': 'test_key'}):
            client = NewsAPIClient()
            results = client.search_news('test')
        
        # Check transformed format
        assert 'title' in results[0]
        assert 'url' in results[0]
        assert 'published_at' in results[0]
        assert 'source' in results[0]
        assert 'description' in results[0]
        assert 'author' in results[0]
    
    @patch('src.news_api.NewsApiClient')
    def test_search_news_custom_days_back(self, mock_newsapi):
        """Test news search with custom days_back parameter."""
        mock_instance = Mock()
        mock_instance.get_everything.return_value = {
            'status': 'ok',
            'articles': []
        }
        mock_newsapi.return_value = mock_instance
        
        with patch.dict(os.environ, {'NEWSAPI_KEY': 'test_key'}):
            client = NewsAPIClient()
            client.search_news('test', language='en', days_back=7)
        
        # Verify the date range is set correctly
        mock_instance.get_everything.assert_called_once()
        call_kwargs = mock_instance.get_everything.call_args[1]
        assert 'from_param' in call_kwargs
        assert 'to' in call_kwargs
