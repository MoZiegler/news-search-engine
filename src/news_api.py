"""
News API integration module.
Handles fetching news articles from NewsAPI.org based on user queries.
"""
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from newsapi import NewsApiClient
from dotenv import load_dotenv
from src.i18n import t


class NewsAPIClient:
    """Client for fetching news articles from NewsAPI.org"""
    
    def __init__(self):
        """Initialize the NewsAPI client with API key from environment."""
        load_dotenv()
        api_key = os.getenv('NEWSAPI_KEY')
        if not api_key or api_key == 'your_api_key_here':
            raise ValueError(
                "NewsAPI key not found or not set. "
                "Please set NEWSAPI_KEY in your .env file. "
                "Get a free key from: https://newsapi.org/register"
            )
        self.client = NewsApiClient(api_key=api_key)
    
    def search_news(
        self, 
        query: str, 
        language: str = 'en',
        days_back: int = 30,
        page_size: int = 100
    ) -> List[Dict]:
        """
        Search for news articles matching the given query.
        
        Args:
            query: Search query/topic
            language: Language code (e.g., 'en', 'de')
            days_back: Number of days to look back
            page_size: Maximum number of articles to retrieve (max 100 per request)
            
        Returns:
            List of article dictionaries containing title, url, publishedAt, source, etc.
        """
        # Calculate date range
        to_date = datetime.now()
        from_date = to_date - timedelta(days=days_back)
        
        try:
            # Search for articles using everything endpoint
            response = self.client.get_everything(
                q=query,
                language=language,
                from_param=from_date.strftime('%Y-%m-%d'),
                to=to_date.strftime('%Y-%m-%d'),
                sort_by='relevancy',  # Sort by relevancy to the query
                page_size=page_size
            )
            
            if response['status'] == 'ok':
                articles = response['articles']
                
                # Clean and normalize article data
                cleaned_articles = []
                for article in articles:
                    cleaned_article = {
                        'title': article.get('title', 'N/A'),
                        'url': article.get('url', 'N/A'),
                        'published_at': article.get('publishedAt', 'N/A'),
                        'source': article.get('source', {}).get('name', 'N/A'),
                        'description': article.get('description', 'N/A'),
                        'author': article.get('author', 'N/A')
                    }
                    cleaned_articles.append(cleaned_article)
                
                return cleaned_articles
            else:
                print(t('errors.newsapi_error', error=response.get('message', 'Unknown error')))
                return []
                
        except Exception as e:
            print(t('errors.fetch_news', error=str(e)))
            return []
    
    def format_published_date(self, date_string: str) -> str:
        """
        Format the published date from ISO format to readable format.
        
        Args:
            date_string: ISO format date string
            
        Returns:
            Formatted date string
        """
        try:
            dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return date_string
