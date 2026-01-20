# How Unit Tests Work

## What Are Unit Tests?

Unit tests are **automated tests** that verify individual "units" (functions, methods, classes) work correctly in isolation. They help catch bugs early and ensure code keeps working as you make changes.

## Basic Structure

Every unit test follows the **AAA pattern**:

1. **Arrange** - Set up test data and conditions
2. **Act** - Execute the function/method being tested
3. **Assert** - Verify the result is what you expected

## (Very) Modified Example from This Project

```python
# filepath: tests/test_csv_handler.py
import pytest
from src.csv_handler import CSVHandler

def test_save_articles_to_csv():
    # ARRANGE - Create test data
    test_articles = [
        {
            'title': 'Test Article 1',
            'url': 'https://example.com/1',
            'publishedAt': '2024-01-15T10:00:00Z',
            'source': {'name': 'Test Source'},
            'author': 'John Doe',
            'description': 'Test description'
        }
    ]
    handler = CSVHandler()
    
    # ACT - Execute the function
    filename = handler.save_articles_to_csv(
        test_articles, 
        'test query', 
        'en'
    )
    
    # ASSERT - Verify it worked
    assert filename.endswith('.csv')  # File was created
    assert 'test_query' in filename   # Query is in filename
    assert os.path.exists(filename)   # File actually exists
    
    # Cleanup
    os.remove(filename)
```

## How pytest Works

### 1. Test Discovery
pytest automatically finds tests by looking for:
- Files named `test_*.py` or `*_test.py`
- Functions named `test_*`
- Classes named `Test*`

### 2. Running Tests
```bash
# Run all tests
pytest

# Run specific file
pytest tests/test_csv_handler.py

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src --cov-report=html
```

### 3. Test Fixtures
Fixtures provide reusable test data:

```python
import pytest

@pytest.fixture
def sample_articles():
    """Fixture that provides test articles to multiple tests."""
    return [
        {'title': 'Article 1', 'url': 'http://test1.com'},
        {'title': 'Article 2', 'url': 'http://test2.com'}
    ]

def test_with_fixture(sample_articles):
    # 'sample_articles' is automatically passed by pytest
    assert len(sample_articles) == 2
    assert sample_articles[0]['title'] == 'Article 1'
```

## Common Assertions

```python
# Equality
assert result == expected
assert result != wrong_value

# Boolean
assert is_valid
assert not is_invalid

# Membership
assert item in collection
assert key in dictionary

# Type checking
assert isinstance(result, str)

# Exceptions
with pytest.raises(ValueError):
    function_that_should_raise_error()

# Approximate equality (for floats)
assert result == pytest.approx(3.14, rel=1e-2)
```

## This Project's Test Structure

```
tests/
├── __init__.py              # Makes 'tests' a package
├── test_csv_handler.py      # Tests CSV export functionality
├── test_entity_extractor.py # Tests NER extraction
├── test_summarizer.py       # Tests headline summarization
└── UNIT_TESTS_EXPLAINED.md  # This file
```

## Example: Testing the Entity Extractor

```python
# filepath: tests/test_entity_extractor.py
import pytest
from src.entity_extractor import EntityExtractor

def test_extract_entities_english():
    # ARRANGE
    extractor = EntityExtractor(language='en')
    articles = [
        {'title': 'Apple releases new iPhone in California'},
        {'title': 'Microsoft and Apple compete in tech market'}
    ]
    
    # ACT
    entities = extractor.extract_entities(articles)
    
    # ASSERT
    assert len(entities) > 0
    # Check that Apple appears (should be recognized as ORG)
    entity_texts = [e[0] for e in entities]
    assert 'Apple' in entity_texts
    
def test_extract_entities_empty_list():
    # ARRANGE
    extractor = EntityExtractor(language='en')
    
    # ACT
    entities = extractor.extract_entities([])
    
    # ASSERT
    assert entities == []  # Should return empty list
```

## Mocking External Dependencies

When testing code that uses APIs or external services, use **mocks** to avoid real API calls:

```python
# filepath: tests/test_news_api.py
import pytest
from unittest.mock import patch, Mock
from src.news_api import NewsAPIClient

@patch('src.news_api.NewsApiClient')  # Mock the external library
def test_search_news(mock_newsapi):
    # ARRANGE - Set up mock response
    mock_instance = Mock()
    mock_instance.get_everything.return_value = {
        'status': 'ok',
        'articles': [
            {'title': 'Test Article', 'url': 'http://test.com'}
        ]
    }
    mock_newsapi.return_value = mock_instance
    
    # ACT
    client = NewsAPIClient()
    results = client.search_news('test query')
    
    # ASSERT
    assert len(results) == 1
    assert results[0]['title'] == 'Test Article'
    # Verify the API was called correctly
    mock_instance.get_everything.assert_called_once()
```

## Running This Project's Tests

```bash
# Activate venv (Windows)
venv\Scripts\activate

# Activate venv (Linux/macOS)
source venv/bin/activate

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/test_csv_handler.py::test_save_articles_to_csv -v

# Run tests in Docker Dev Container
# (automatically available in the container terminal)
pytest
```

## Benefits of Unit Tests

✅ **Catch bugs early** - Before they reach production  
✅ **Document behavior** - Tests show how code should work  
✅ **Enable refactoring** - Change code confidently  
✅ **Regression prevention** - Ensure old bugs don't return  
✅ **Faster debugging** - Pinpoint exactly what broke  

## Key Principles

1. **Tests should be independent** - Don't rely on other tests
2. **Tests should be fast** - Mock slow operations (API calls, DB)
3. **Tests should be deterministic** - Same input = same output
4. **One assertion per concept** - Keep tests focused
5. **Use descriptive names** - `test_save_csv_creates_file_with_timestamp()`

## Test Coverage in This Project

The project includes comprehensive unit tests for core modules:

- **CSV Handler** (`test_csv_handler.py`) - Validates CSV file creation and data formatting
- **Entity Extractor** (`test_entity_extractor.py`) - Tests Named Entity Recognition
- **Summarizer** (`test_summarizer.py`) - Verifies headline summarization

These tests ensure components work correctly in isolation and continue to work as the codebase evolves.

## Best Practices Demonstrated

### 1. Class-Based Test Organization
```python
class TestSummarizer:
    """Test cases for Summarizer class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.summarizer = Summarizer()
```

### 2. Descriptive Test Names
- `test_summarize_headlines_basic` - Clear what's being tested
- `test_extract_entities_empty_list` - Documents edge case

### 3. Testing Edge Cases
- Empty inputs
- Missing data
- Invalid formats
- Error conditions

### 4. Cleanup After Tests
```python
# Always clean up test artifacts
os.remove(filename)
```

## Further Reading

- [pytest Documentation](https://docs.pytest.org/)
- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)
- [Test-Driven Development (TDD)](https://en.wikipedia.org/wiki/Test-driven_development)