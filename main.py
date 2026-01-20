#!/usr/bin/env python3
"""
News Search Engine - Main Application
Interactive CLI for searching and analyzing news articles.
"""
import sys
from src.news_api import NewsAPIClient
from src.csv_handler import CSVHandler
from src.summarizer import Summarizer
from src.entity_extractor import EntityExtractor
from src.i18n import set_language, t


class NewsSearchEngine:
    """Main application class for the news search engine."""
    
    def __init__(self):
        """Initialize the news search engine components."""
        try:
            self.news_client = NewsAPIClient()
            self.csv_handler = CSVHandler()
            self.summarizer = Summarizer()
            print("\n" + "=" * 70)
            print(f"         {t('app.welcome')}")
            print("=" * 70)
        except ValueError as e:
            print(f"\n{t('errors.initialization', error=str(e))}")
            sys.exit(1)
    
    def get_language_choice(self) -> str:
        """
        Prompt user to select a language for the search.
        
        Returns:
            Language code ('en' or 'de')
        """
        print("\n" + "=" * 70)
        print(f"{t('language.select')}")
        print("=" * 70)
        print(f"  1. {t('language.english')}")
        print(f"  2. {t('language.german')}")
        
        while True:
            choice = input(f"\n{t('language.prompt')}").strip()
            
            if  choice == '1':
                print(f"✓ {t('language.selected')}: {t('language.english')}")
                return 'en'
            elif choice == '2':
                print(f"✓ {t('language.selected')}: {t('language.german')}")
                return 'de'
            elif choice.lower() in ['quit', 'exit', 'q']:
                return '0'
            else:
                print(t('language.invalid'))
    
    def search_and_display(self, query: str, language: str = 'en'):
        """
        Search for news articles and display results.
        
        Args:
            query: Search topic/query
            language: Language code for search
        """
        # Set UI language to match search language
        set_language(language)
        
        print(f"\n{t('search.searching', query=query, language=language)}")
        print(f"{t('search.please_wait')}\n")
        
        # Fetch articles
        articles = self.news_client.search_news(query, language=language)
        
        if not articles:
            print(t('search.no_results'))
            return
        
        print(t('search.found', count=len(articles)))
        
        # Save all articles to CSV
        csv_file = self.csv_handler.save_articles_to_csv(articles, query, language)
        
        # Display top 15 articles
        top_15 = articles[:15]
        self._display_top_articles(top_15)
        
        # Generate and display summary
        print("\n" + "=" * 70)
        print(t('display.summary'))
        print("=" * 70)
        summary = self.summarizer.summarize_headlines(top_15)
        print(summary)
        
        # Extract and display named entities
        print("\n" + "=" * 70)
        print(t('display.entities'))
        print("=" * 70)
        entity_extractor = EntityExtractor(language=language)
        entities = entity_extractor.extract_entities(top_15)
        entities_output = entity_extractor.format_entities_output(entities)
        print(entities_output)
        
        # Display CSV file information
        if csv_file:
            print("\n" + "=" * 70)
            print(t('display.saved', count=len(articles), file=csv_file))
            print("=" * 70)
    
    def _display_top_articles(self, articles: list):
        """
        Display the top articles in a formatted way.
        
        Args:
            articles: List of article dictionaries
        """
        print("\n" + "=" * 70)
        print(t('display.top_articles'))
        print("=" * 70 + "\n")
        
        for i, article in enumerate(articles, 1):
            title = article.get('title', 'N/A')
            url = article.get('url', 'N/A')
            published = article.get('published_at', 'N/A')
            source = article.get('source', 'N/A')
            
            # Format published date
            if published != 'N/A':
                published = self.news_client.format_published_date(published)
            
            print(f"{i}. {title}")
            print(f"   {t('display.source')}: {source}")
            print(f"   {t('display.published')}: {published}")
            print(f"   URL: {url}")
            print()
    
    def run(self):
        """Run the main application loop."""
        while True:
            try:
                print("\n" + "=" * 70)
                
                # Get language preference
                language = self.get_language_choice()
                if language == '0':
                    print(f"\n👋 {t('app.goodbye')}")
                    break

                #set language in i18n module
                set_language(language)
                
                # Get search query
                print("\n" + "=" * 70)
                query = input(f"\n{t('search.prompt')}").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print(f"\n👋 {t('app.goodbye')}")
                    break
                
                if not query:
                    print(t('search.invalid_topic'))
                    continue
                
                # Perform search and display results
                self.search_and_display(query, language)
                
                # Ask if user wants to continue
                print("\n" + "=" * 70)
                continue_choice = input(f"\n{t('search.another')}").strip().lower()
                
                if continue_choice in ['n', 'no', 'nein']:
                    print(f"\n👋 {t('app.goodbye')}")
                    break
                    
            except KeyboardInterrupt:
                print(f"\n\n👋 {t('app.interrupted')}")
                break
            except Exception as e:
                print(f"\n{t('errors.general', error=str(e))}")
                print(t('errors.retry'))


def main():
    """Main entry point for the application."""
    try:
        app = NewsSearchEngine()
        app.run()
    except Exception as e:
        print(f"\n{t('errors.fatal', error=str(e))}")
        sys.exit(1)


if __name__ == "__main__":
    main()
