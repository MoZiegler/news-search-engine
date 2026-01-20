# What `conftest.py` Does

## Purpose

`conftest.py` is a **special pytest file** that contains **shared fixtures and configuration** that can be used across all test files in the directory and subdirectories.

## Key Features

### 1. **Shared Fixtures**
Define fixtures once, use them in any test file without importing:

```python
# filepath: tests/conftest.py
import pytest

@pytest.fixture
def sample_articles():
    """Shared fixture for sample articles used across multiple tests."""
    return [
        {
            'title': 'Test Article 1',
            'url': 'https://example.com/1',
            'publishedAt': '2026-01-15T10:00:00Z',
            'source': {'name': 'Test Source'},
            'author': 'John Doe',
            'description': 'Test description 1'
        },
        {
            'title': 'Test Article 2',
            'url': 'https://example.com/2',
            'publishedAt': '2026-01-16T12:00:00Z',
            'source': {'name': 'Another Source'},
            'author': 'Jane Smith',
            'description': 'Test description 2'
        }
    ]

@pytest.fixture
def mock_api_key(monkeypatch):
    """Mock API key for testing without real credentials."""
    monkeypatch.setenv('NEWSAPI_KEY', 'test_api_key_12345')
```

### 2. **Using Shared Fixtures**
No import needed - pytest automatically discovers them:

```python
# filepath: tests/test_csv_handler.py
def test_save_articles(sample_articles):  # Automatically available!
    handler = CSVHandler()
    filename = handler.save_articles_to_csv(sample_articles, 'test', 'en')
    assert filename.endswith('.csv')
```

```python
# filepath: tests/test_summarizer.py
def test_summarize(sample_articles):  # Same fixture, different file!
    summarizer = Summarizer()
    summary = summarizer.summarize_headlines(sample_articles)
    assert summary is not None
```

### 3. **Pytest Configuration**
Configure pytest behavior:

```python
# filepath: tests/conftest.py
import pytest

def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )

@pytest.fixture(autouse=True)
def reset_environment():
    """Automatically reset environment before each test."""
    import os
    # Save original env
    original_env = os.environ.copy()
    
    yield  # Run the test
    
    # Restore original env after test
    os.environ.clear()
    os.environ.update(original_env)
```

### 4. **Test Data Loading**
Load shared test data files:

```python
# filepath: tests/conftest.py
import pytest
import json
from pathlib import Path

@pytest.fixture
def sample_data_from_file():
    """Load sample data from JSON file."""
    fixtures_dir = Path(__file__).parent / 'fixtures'
    with open(fixtures_dir / 'sample_data.json', 'r') as f:
        return json.load(f)
```

## Benefits

### ✅ **DRY Principle** (Don't Repeat Yourself)
Define test data once, use everywhere:
```python
# Without conftest.py - Repeated in every test file
def test_a():
    articles = [{'title': '...'}]  # Duplicated
    
def test_b():
    articles = [{'title': '...'}]  # Duplicated

# With conftest.py - Defined once
@pytest.fixture
def sample_articles():
    return [{'title': '...'}]
```

### ✅ **Consistency**
All tests use the same test data

### ✅ **Maintenance**
Update test data in one place

### ✅ **Organization**
Separates test logic from test data

## Example for Your Project

```python
# filepath: tests/conftest.py
"""
Shared pytest fixtures and configuration for all tests.
"""
import pytest
import os
from pathlib import Path


@pytest.fixture
def sample_articles():
    """
    Standard sample articles fixture used across multiple test files.
    
    Returns:
        List of article dictionaries with all required fields.
    """
    return [
        {
            'title': 'Artificial Intelligence Transforms Healthcare Industry',
            'url': 'https://example.com/ai-healthcare',
            'publishedAt': '2026-01-15T10:30:00Z',
            'source': {'name': 'Tech News Daily'},
            'author': 'Dr. Jane Smith',
            'description': 'AI is revolutionizing medical diagnosis and treatment.'
        },
        {
            'title': 'Climate Summit Reaches Historic Agreement',
            'url': 'https://example.com/climate-summit',
            'publishedAt': '2026-01-16T14:20:00Z',
            'source': {'name': 'World News'},
            'author': 'John Doe',
            'description': 'World leaders commit to carbon neutrality by 2050.'
        },
        {
            'title': 'Stock Markets Hit Record Highs Amid Economic Growth',
            'url': 'https://example.com/stock-markets',
            'publishedAt': '2026-01-17T09:15:00Z',
            'source': {'name': 'Financial Times'},
            'author': 'Sarah Johnson',
            'description': 'Global markets surge on positive economic indicators.'
        }
    ]


@pytest.fixture
def mock_newsapi_key(monkeypatch):
    """
    Mock the NEWSAPI_KEY environment variable for testing.
    
    Automatically sets a fake API key for tests that need it.
    """
    monkeypatch.setenv('NEWSAPI_KEY', 'test_api_key_abc123xyz')


@pytest.fixture
def temp_output_dir(tmp_path):
    """
    Create a temporary output directory for test files.
    
    Args:
        tmp_path: pytest's built-in temporary directory fixture
        
    Returns:
        Path to temporary output directory
    """
    output_dir = tmp_path / "test_output"
    output_dir.mkdir()
    return output_dir


@pytest.fixture(autouse=True)
def cleanup_csv_files():
    """
    Automatically clean up any CSV files created during tests.
    
    Runs before and after each test automatically.
    """
    # Setup: Nothing needed before test
    yield
    
    # Teardown: Remove CSV files after test
    current_dir = Path.cwd()
    for csv_file in current_dir.glob('news_*.csv'):
        try:
            csv_file.unlink()
        except:
            pass


@pytest.fixture
def sample_translations():
    """
    Sample translation data for i18n tests.
    
    Returns:
        Dictionary with sample English and German translations
    """
    return {
        'en': {
            'app': {
                'title': 'News Search Engine',
                'welcome': 'Welcome to News Search Engine'
            },
            'search': {
                'prompt': 'Enter search query',
                'found': 'Found {count} articles'
            }
        },
        'de': {
            'app': {
                'title': 'Nachrichten-Suchmaschine',
                'welcome': 'Willkommen zur Nachrichten-Suchmaschine'
            },
            'search': {
                'prompt': 'Suchanfrage eingeben',
                'found': '{count} Artikel gefunden'
            }
        }
    }


# Pytest configuration
def pytest_configure(config):
    """Add custom markers for test organization."""
    config.addinivalue_line(
        "markers", 
        "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers",
        "integration: marks tests requiring external services"
    )
    config.addinivalue_line(
        "markers",
        "unit: marks tests as unit tests (default)"
    )
```

## Usage Examples

### In test_csv_handler.py:
```python
def test_save_articles(sample_articles, temp_output_dir):
    # sample_articles and temp_output_dir automatically available!
    handler = CSVHandler()
    # ... test code
```

### In test_news_api.py:
```python
def test_search_news(mock_newsapi_key, sample_articles):
    # API key is mocked, sample_articles available
    client = NewsAPIClient()
    # ... test code
```

### In test_i18n.py:
```python
def test_translations(sample_translations):
    # Translation data automatically available
    translator = Translator()
    # ... test code
```

## Key Advantages

1. **No imports needed** - Fixtures are auto-discovered
2. **Centralized setup** - One place for all shared test resources
3. **Automatic cleanup** - `autouse=True` fixtures run automatically
4. **Scope control** - Can be function, class, module, or session-scoped
5. **Dependency injection** - pytest automatically provides fixture values

## Scopes

```python
@pytest.fixture(scope='function')  # Default - new instance per test
def per_test_fixture():
    return "recreated for each test"

@pytest.fixture(scope='class')  # Shared within test class
def per_class_fixture():
    return "shared across class tests"

@pytest.fixture(scope='module')  # Shared within file
def per_module_fixture():
    return "shared across entire test file"

@pytest.fixture(scope='session')  # Shared across all tests
def per_session_fixture():
    return "created once for entire test session"
```

## TODO: Implementation

This project currently does NOT have a `conftest.py` file. To implement shared fixtures:

1. Create `tests/conftest.py`
2. Move duplicate test data (like `sample_articles`) into shared fixtures
3. Update existing test files to use the shared fixtures
4. Add automatic cleanup fixtures for CSV files
5. Add mock environment variable fixtures

This will reduce code duplication across test files and make tests more maintainable.

**TL;DR:** `conftest.py` is pytest's way of sharing test fixtures, configuration, and setup code across all your tests without needing explicit imports. It keeps tests DRY and organized!
