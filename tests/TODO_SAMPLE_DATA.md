# What `sample_data.json` Contains

## Purpose

`sample_data.json` in the `fixtures/` directory typically contains **static test data** that's used across multiple tests. It's a way to externalize test data from Python code.

## Common Contents

For a news search engine project, it would typically contain:

### Example Structure:

```json
{
  "articles": [
    {
      "title": "Artificial Intelligence Breakthrough in Medical Diagnostics",
      "url": "https://example.com/ai-medical-breakthrough",
      "publishedAt": "2026-01-15T10:30:00Z",
      "source": {
        "id": "techcrunch",
        "name": "TechCrunch"
      },
      "author": "Dr. Sarah Johnson",
      "description": "Researchers develop AI system that can detect diseases with 95% accuracy.",
      "content": "Full article content here...",
      "urlToImage": "https://example.com/image.jpg"
    },
    {
      "title": "Climate Summit Reaches Historic Agreement",
      "url": "https://example.com/climate-summit-2026",
      "publishedAt": "2026-01-16T14:20:00Z",
      "source": {
        "id": "bbc-news",
        "name": "BBC News"
      },
      "author": "Environmental Correspondent",
      "description": "World leaders commit to ambitious carbon reduction targets.",
      "content": "At the annual climate summit...",
      "urlToImage": "https://example.com/climate.jpg"
    },
    {
      "title": "Stock Markets Surge on Economic Data",
      "url": "https://example.com/markets-surge",
      "publishedAt": "2026-01-17T09:15:00Z",
      "source": {
        "id": "financial-times",
        "name": "Financial Times"
      },
      "author": "Market Analyst Team",
      "description": "Global markets hit record highs following positive economic indicators.",
      "content": "Stock markets around the world...",
      "urlToImage": "https://example.com/stocks.jpg"
    }
  ],
  "api_responses": {
    "success": {
      "status": "ok",
      "totalResults": 87,
      "articles": "..."
    },
    "error": {
      "status": "error",
      "code": "apiKeyInvalid",
      "message": "Your API key is invalid or incorrect."
    },
    "empty": {
      "status": "ok",
      "totalResults": 0,
      "articles": []
    }
  },
  "translations": {
    "test_keys": {
      "en": {
        "greeting": "Hello",
        "farewell": "Goodbye"
      },
      "de": {
        "greeting": "Hallo",
        "farewell": "Auf Wiedersehen"
      }
    }
  },
  "entities": {
    "expected": [
      {"text": "Apple", "type": "ORG", "count": 3},
      {"text": "New York", "type": "GPE", "count": 2},
      {"text": "Biden", "type": "PERSON", "count": 1}
    ]
  }
}
```

## Why Use JSON Fixtures?

### ✅ **Advantages:**

1. **Separation of Concerns** - Data separate from test logic
2. **Readability** - Easy to view and edit test data
3. **Reusability** - Same data across multiple tests
4. **Version Control** - Track changes to test data
5. **Large Datasets** - Better than hardcoding in Python files
6. **Realistic Data** - Can use actual API responses

### ❌ **When NOT to Use:**

- Simple, small test cases (use Python fixtures instead)
- Dynamically generated data (use Python functions)
- Data that needs computation

## Loading in conftest.py

```python
# filepath: tests/conftest.py
import pytest
import json
from pathlib import Path

@pytest.fixture
def sample_data():
    """Load sample data from JSON file."""
    fixtures_dir = Path(__file__).parent / 'fixtures'
    with open(fixtures_dir / 'sample_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@pytest.fixture
def sample_articles(sample_data):
    """Extract just the articles from sample data."""
    return sample_data['articles']

@pytest.fixture
def mock_api_success_response(sample_data):
    """Get mock successful API response."""
    return sample_data['api_responses']['success']

@pytest.fixture
def mock_api_error_response(sample_data):
    """Get mock error API response."""
    return sample_data['api_responses']['error']
```

## Usage in Tests

```python
# filepath: tests/test_csv_handler.py
def test_save_articles(sample_articles):
    """Test saving articles from fixture file."""
    handler = CSVHandler()
    filename = handler.save_articles_to_csv(sample_articles, 'test', 'en')
    assert filename.endswith('.csv')
```

```python
# filepath: tests/test_news_api.py
from unittest.mock import Mock, patch

def test_api_success(mock_api_success_response):
    """Test handling successful API response."""
    mock_client = Mock()
    mock_client.get_everything.return_value = mock_api_success_response
    # ... test code
```

## Your Project

**Current Status:** You don't have a `fixtures/` directory or `sample_data.json` yet.

**Should you create it?** 

- ✅ **YES** - If you want to reduce hardcoded data in test files
- ✅ **YES** - If you want realistic NewsAPI response examples
- ✅ **YES** - If tests are getting cluttered with data setup

## Example for Your Project

```json
{
  "newsapi_articles": [
    {
      "title": "Python 3.13 Released with Performance Improvements",
      "url": "https://example.com/python-313",
      "publishedAt": "2026-01-15T10:00:00Z",
      "source": {"name": "Tech News"},
      "author": "Python Core Team",
      "description": "Latest Python version brings significant speed improvements."
    },
    {
      "title": "Docker Compose Simplifies Container Orchestration",
      "url": "https://example.com/docker-compose",
      "publishedAt": "2026-01-16T12:00:00Z",
      "source": {"name": "DevOps Weekly"},
      "author": "Container Expert",
      "description": "New Docker Compose features make multi-container apps easier."
    }
  ],
  "csv_test_data": {
    "valid_articles": [
      {
        "title": "Valid Article 1",
        "url": "https://example.com/1",
        "publishedAt": "2026-01-15T10:00:00Z",
        "source": {"name": "Test Source"},
        "author": "Test Author",
        "description": "Test description"
      }
    ],
    "empty_articles": [],
    "malformed_articles": [
      {
        "title": null,
        "url": "invalid-url",
        "publishedAt": "not-a-date"
      }
    ]
  },
  "entity_extraction_test_cases": {
    "headlines_with_entities": [
      "Apple releases new iPhone in California",
      "Microsoft CEO Satya Nadella speaks in Seattle",
      "President Biden visits New York"
    ],
    "expected_entities": [
      {"text": "Apple", "type": "ORG"},
      {"text": "California", "type": "GPE"},
      {"text": "Microsoft", "type": "ORG"},
      {"text": "Satya Nadella", "type": "PERSON"},
      {"text": "Seattle", "type": "GPE"},
      {"text": "Biden", "type": "PERSON"},
      {"text": "New York", "type": "GPE"}
    ]
  },
  "summarization_test_cases": {
    "short_headlines": [
      "Markets rise",
      "Weather improves",
      "Tech stocks gain"
    ],
    "long_headlines": [
      "Comprehensive climate change report reveals urgent need for immediate action across all sectors",
      "Revolutionary artificial intelligence system demonstrates unprecedented capabilities in natural language understanding",
      "Global economic summit produces historic agreement on international trade policies and regulations"
    ]
  }
}
```

## TODO: Implementation

To implement this in your project:

1. **Create the directory:**
   ```bash
   mkdir tests/fixtures
   ```

2. **Create `tests/fixtures/sample_data.json`** with realistic test data

3. **Create `tests/conftest.py`** with fixtures to load the data

4. **Refactor existing tests** to use the shared fixtures instead of hardcoded data

5. **Benefits:**
   - Cleaner test files
   - Easier to maintain test data
   - More realistic test scenarios
   - Better test organization

**TL;DR:** `sample_data.json` contains static test data (articles, API responses, etc.) in JSON format that's loaded by pytest fixtures and used across multiple test files. It's currently just an example in the file structure - you haven't created it yet in your project, but it would help reduce code duplication in your tests.
