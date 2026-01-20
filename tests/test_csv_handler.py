"""
Unit tests for CSV handler module.
"""
import pytest
import os
import pandas as pd
from unittest.mock import patch
from src.csv_handler import CSVHandler


class TestCSVHandler:
    """Test cases for CSVHandler class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.csv_handler = CSVHandler()
        self.sample_articles = [
            {
                'title': 'Test Article 1',
                'url': 'https://example.com/article1',
                'published_at': '2026-01-15T10:00:00Z',
                'source': 'Test Source',
                'author': 'Test Author',
                'description': 'Test description'
            },
            {
                'title': 'Test Article 2',
                'url': 'https://example.com/article2',
                'published_at': '2026-01-16T12:00:00Z',
                'source': 'Another Source',
                'author': 'Another Author',
                'description': 'Another description'
            }
        ]
        self.test_output_dir = 'test_output'
    
    def teardown_method(self):
        """Clean up test files and directories."""
        # Remove any CSV files created during tests in current directory
        for file in os.listdir('.'):
            if file.startswith('news_') and file.endswith('.csv'):
                try:
                    os.remove(file)
                except:
                    pass
        
        # Remove test output directory if it exists
        if os.path.exists(self.test_output_dir):
            for file in os.listdir(self.test_output_dir):
                if file.startswith('news_') and file.endswith('.csv'):
                    try:
                        os.remove(os.path.join(self.test_output_dir, file))
                    except:
                        pass
            try:
                os.rmdir(self.test_output_dir)
            except:
                pass
    
    def test_save_articles_to_csv_default_directory(self):
        """Test saving articles to CSV file in default directory (venv case)."""
        # Ensure OUTPUT_DIR is not set
        # temporarily unset OUTPUT_DIR in the environment if it exists
        with patch.dict(os.environ, {}, clear=True):
            filename = self.csv_handler.save_articles_to_csv(
                self.sample_articles, 
                'test_query', 
                'en'
            )
            
            assert filename != ""
            assert os.path.exists(filename)
            assert filename.endswith('.csv')
            # Should be in current directory
            assert os.path.dirname(filename) == '.' or os.path.dirname(filename) == ''
            
            # Verify file contents using pandas
            df = pd.read_csv(filename)
            assert len(df) == 2
            assert df.iloc[0]['Title'] == 'Test Article 1'
        with patch.dict(os.environ, {}, clear=True):
            filename = self.csv_handler.save_articles_to_csv([], 'test', 'en')
            assert filename == ""
    
    def test_validate_csv_file_default_directory(self):
        """Test CSV file validation in default directory."""
        with patch.dict(os.environ, {}, clear=True):
            # Create a valid CSV file
            filename = self.csv_handler.save_articles_to_csv(
                self.sample_articles,
                'test',
                'en'
            )
            
            assert self.csv_handler.validate_csv_file(filename) == True
            assert self.csv_handler.validate_csv_file('nonexistent.csv') == False
    
    def test_validate_csv_file_with_output_dir(self):
        """Test CSV file validation with OUTPUT_DIR set."""
        # Ensure OUTPUT_DIR is set
        # temporarily set OUTPUT_DIR in the environment
        with patch.dict(os.environ, {'OUTPUT_DIR': self.test_output_dir}):
            # Create a valid CSV file
            filename = self.csv_handler.save_articles_to_csv(
                self.sample_articles,
                'test',
                'en'
            )
            
            assert self.csv_handler.validate_csv_file(filename) == True
            assert self.csv_handler.validate_csv_file('nonexistent.csv') == False
    
    def test_filename_contains_query_and_language(self):
        """Test that filename includes query and language parameters."""
        with patch.dict(os.environ, {'OUTPUT_DIR': self.test_output_dir}):
            filename = self.csv_handler.save_articles_to_csv(
                self.sample_articles,
                'artificial intelligence',
                'de'
            )
            
            # Check filename contains sanitized query and language
            basename = os.path.basename(filename)
            assert 'artificial_intelligence' in basename
            assert '_de_' in basename
            assert basename.endswith('.csv')
            assert filename.endswith('.csv')
            # Should be in the OUTPUT_DIR directory
            assert filename.startswith(self.test_output_dir)
            assert os.path.dirname(filename) == self.test_output_dir
            
            # Verify file contents using pandas
            df = pd.read_csv(filename)
            assert len(df) == 2
            assert df.iloc[0]['Title'] == 'Test Article 1'
            assert df.iloc[1]['Title'] == 'Test Article 2'
    
    def test_output_directory_created_if_not_exists(self):
        """Test that OUTPUT_DIR is created if it doesn't exist (Docker case)."""
        nonexistent_dir = 'test_nonexistent_output'
        
        # Ensure directory doesn't exist before test
        if os.path.exists(nonexistent_dir):
            os.rmdir(nonexistent_dir)
        
        with patch.dict(os.environ, {'OUTPUT_DIR': nonexistent_dir}):
            filename = self.csv_handler.save_articles_to_csv(
                self.sample_articles,
                'test_query',
                'en'
            )
            
            # Directory should have been created
            assert os.path.exists(nonexistent_dir)
            assert os.path.isdir(nonexistent_dir)
            assert filename.startswith(nonexistent_dir)
            
            # Cleanup
            if os.path.exists(filename):
                os.remove(filename)
            if os.path.exists(nonexistent_dir):
                os.rmdir(nonexistent_dir)
    
    def test_save_empty_articles(self):
        """Test saving empty articles list."""
        filename = self.csv_handler.save_articles_to_csv([], 'test', 'en')
        assert filename == ""
    
    def test_validate_csv_file(self):
        """Test CSV file validation."""
        # Create a valid CSV file
        filename = self.csv_handler.save_articles_to_csv(
            self.sample_articles,
            'test',
            'en'
        )
        
        assert self.csv_handler.validate_csv_file(filename) == True
        assert self.csv_handler.validate_csv_file('nonexistent.csv') == False
