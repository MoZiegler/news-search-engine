"""
Summarizer module.
Handles generating summaries of news article headlines using transformers.
"""
from typing import List, Dict
from transformers import pipeline
import warnings
from src.i18n import t

# Suppress warnings from transformers
warnings.filterwarnings('ignore')


class Summarizer:
    """Generates summaries of news article headlines."""
    
    def __init__(self):
        """Initialize the summarization pipeline."""
        self.pipeline = None
    
    def _initialize_pipeline(self):
        """Lazy initialization of the summarization pipeline."""
        if self.pipeline is None:
            print(t('summarizer.loading'))
            try:
                # Using a lightweight model suitable for summarization
                self.pipeline = pipeline(
                    "summarization",
                    model="facebook/bart-large-cnn",
                    device=-1  # Use CPU
                )
                print(t('summarizer.loaded'))
            except Exception as e:
                print(t('summarizer.error', error=str(e)))
                self.pipeline = None
    
    def summarize_headlines(self, articles: List[Dict], max_length: int = 150) -> str:
        """
        Generate a summary of article headlines.
        
        Args:
            articles: List of article dictionaries containing 'title' field
            max_length: Maximum length of the summary
            
        Returns:
            Summary text
        """
        if not articles:
            return t('summarizer.no_articles')
        
        # Combine all headlines into one text
        headlines = [article.get('title', '') for article in articles if article.get('title')]
        
        if not headlines:
            return t('summarizer.no_headlines')
        
        # Join headlines with periods
        combined_text = ". ".join(headlines) + "."
        
        # If text is too short, return as is
        if len(combined_text.split()) < 50:
            return f"Combined Headlines: {combined_text}"
        
        # Try to use the transformer model
        self._initialize_pipeline()
        
        if self.pipeline:
            try:
                # Limit input size to avoid token limit issues
                max_input_length = 1024
                if len(combined_text) > max_input_length:
                    # Truncate text intelligently at sentence boundaries
                    combined_text = combined_text[:max_input_length]
                    last_period = combined_text.rfind('.')
                    if last_period > 0:
                        combined_text = combined_text[:last_period + 1]
                
                summary = self.pipeline(
                    combined_text,
                    max_length=max_length,
                    min_length=30,
                    do_sample=False
                )
                
                return summary[0]['summary_text']
                
            except Exception as e:
                print(t('summarizer.fallback_error', error=str(e)))
                return self._fallback_summary(headlines)
        else:
            return self._fallback_summary(headlines)
    
    def _fallback_summary(self, headlines: List[str]) -> str:
        """
        Fallback summary method using simple extraction.
        
        Args:
            headlines: List of headline strings
            
        Returns:
            Simple summary text
        """
        # Take first 3-5 headlines as representative summary
        num_headlines = min(5, len(headlines))
        sample_headlines = headlines[:num_headlines]
        
        summary = t('summarizer.fallback_title') + "\n"
        for i, headline in enumerate(sample_headlines, 1):
            summary += f"{i}. {headline}\n"
        
        return summary.strip()
