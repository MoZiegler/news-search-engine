"""
CSV handler module.
Handles writing news articles to CSV files using pandas.
"""
import pandas as pd
from datetime import datetime
from typing import List, Dict
import os
from src.i18n import t


class CSVHandler:
    """Handles CSV file operations for news articles."""
    
    @staticmethod
    def save_articles_to_csv(articles: List[Dict], query: str, language: str) -> str:
        """
        Save articles to a CSV file using pandas.
        
        Args:
            articles: List of article dictionaries
            query: Search query used
            language: Language code used
            
        Returns:
            Path to the created CSV file
        """
        if not articles:
            print(t('csv.no_articles'))
            return ""
        
        # Create output directory if it doesn't exist (for Docker support)
        # Uses OUTPUT_DIR env var if set (Docker), otherwise defaults to current directory (venv)
        # This ensures compatibility with both containerized and local development environments
        output_dir = os.environ.get('OUTPUT_DIR', '.')
        os.makedirs(output_dir, exist_ok=True)
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_query = "".join(c if c.isalnum() else "_" for c in query)[:30]
        filename = os.path.join(output_dir, f"news_{safe_query}_{language}_{timestamp}.csv")
        
        try:
            # Create DataFrame from articles
            df = pd.DataFrame([{
                'Title': article.get('title', 'N/A'),
                'URL': article.get('url', 'N/A'),
                'Published Date': article.get('published_at', 'N/A'),
                'Source': article.get('source', 'N/A'),
                'Author': article.get('author', 'N/A'),
                'Description': article.get('description', 'N/A')
            } for article in articles])
            
            # Save to CSV
            df.to_csv(filename, index=False, encoding='utf-8')
            
            print(f"\n{t('csv.saved', filename=filename)}")
            return filename
            
        except Exception as e:
            print(t('csv.error', error=str(e)))
            return ""
    
    @staticmethod
    def validate_csv_file(filename: str) -> bool:
        """
        Validate that a CSV file exists and is readable using pandas.
        
        Args:
            filename: Path to the CSV file
            
        Returns:
            True if file is valid, False otherwise
        """
        if not os.path.exists(filename):
            return False
        
        try:
            pd.read_csv(filename, nrows=1)
            return True
        except:
            return False
