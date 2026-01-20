# CLI News Search Engine (Python)

A Python-based news search engine that allows users to search for recent news articles on any topic, with automatic summarization and named entity recognition.

## Features

- 🔍 Search for news articles on any topic
- 🌍 Support for multiple languages (English and German)
- 📊 Displays top-15 most relevant articles sorted by relevancy
- 💾 Exports all results to CSV file automatically
- 📝 Automatic summarization of top headlines
- 🏷️ Named Entity Recognition (NER) with frequency analysis
- 🔄 Interactive CLI for multiple searches in one session
- 🌐 Full internationalization (i18n) support
- 🐳 Docker and Dev Container support
- ✅ Comprehensive unit tests


## Project Structure

```
news-search-engine/
├── .devcontainer/
│   └── devcontainer.json          # VS Code Dev Container configuration
├── .github/
│   └── workflows/
│       └── tests.yml              # GitHub Actions CI/CD workflow (optional)
├── src/
│   ├── __init__.py                # Package initialization
│   ├── csv_handler.py             # CSV export functionality
│   ├── entity_extractor.py        # Named Entity Recognition (NER)
│   ├── i18n.py                    # Internationalization module
│   ├── news_api.py                # NewsAPI client wrapper
│   └── summarizer.py              # Headline summarization
├── tests/
│   ├── __init__.py                # Test package initialization
│   ├── test_csv_handler.py        # CSV handler unit tests
│   ├── test_entity_extractor.py   # Entity extractor unit tests
│   ├── test_i18n.py               # i18n module unit tests
│   ├── test_news_api.py           # News API client unit tests
│   ├── test_summarizer.py         # Summarizer unit tests
│   ├── UNIT_TESTS_EXPLAINED.md    # Unit testing documentation
│   ├── TODO_CONFTEST.md           # Guide for implementing conftest.py
│   └── TODO_SAMPLE_DATA.md        # Guide for implementing test fixtures
├── translations/
│   ├── en.json                    # English translations
│   └── de.json                    # German translations
├── output/                        # Generated CSV files (gitignored)
├── .dockerignore                  # Files to exclude from Docker build
├── .env                           # Environment variables (gitignored)
├── .env.example                   # Example environment configuration
├── .gitignore                     # Git ignore rules
├── docker-compose.yml             # Docker Compose configuration
├── Dockerfile                     # Docker container definition
├── main.py                        # Main application entry point
├── README.md                      # This file
└── requirements.txt               # Python dependencies
```

## Requirements

- **Option 1 (Local)**: Python 3.12
- **Option 2 (Dev Container)**: Docker, VS Code with Dev Containers extension
- **Option 3 (Docker)**: Docker and Docker Compose
- NewsAPI key (free tier available)

## Installation

### Option 1: Local Installation with venv

**Important:** This project uses Python's built-in `venv` module (NOT Conda).

1. **Navigate to the project directory:**
   ```bash
   cd news-search-engine
   ```

2. **Create a virtual environment:**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate the virtual environment
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   (On Windows, Pytorch requires Microsoft Visual C++ Redistributables)

4. **Download spaCy language models:**
   ```bash
   # For English support:
   python -m spacy download en_core_web_sm
   
   # For German support (optional):
   python -m spacy download de_core_news_sm
   ```

5. **Set up your NewsAPI key:**
   ```bash
   # On Windows:
   copy .env.example .env
   
   # On macOS/Linux:
   cp .env.example .env
   ```
   
   Edit the `.env` file and add your API key from [NewsAPI.org](https://newsapi.org/register):
   ```
   NEWSAPI_KEY=your_actual_api_key_here
   ```

**Important:** Never commit your `.env` file to version control. It's already included in `.gitignore`.


### Option 2: VS Code Dev Container (Best for Development)

Dev Containers provide the best development experience with instant code sync, debugging, and pre-configured extensions.

**Prerequisites:**
- VS Code with "Dev Containers" extension installed
- Docker and Docker Compose installed

**Steps:**

1. **Set up NewsAPI key:**
   ```bash
   # On Windows:
   copy .env.example .env
   
   # On macOS/Linux:
   cp .env.example .env
   
   # Edit .env and add your API key from https://newsapi.org/register
   ```

2. **Open in Dev Container:**
   - Open the project folder in VS Code
   - Press `F1` or `Ctrl+Shift+P`
   - Select **"Dev Containers: Reopen in Container"**
   - Wait for the container to build (first time takes a few minutes)

3. **Run the application:**
   ```bash
   # In the VS Code integrated terminal
   python main.py
   ```

**Benefits:**
- ✅ Consistent development environment across all team members
- ✅ All dependencies and tools pre-installed
- ✅ Python extensions configured automatically
- ✅ Direct code editing with instant sync
- ✅ Integrated debugging and testing
- ✅ No need for local Python/venv setup

### Option 3: Docker Compose (Production-Ready)

Docker provides a consistent environment and is ideal for 12-factor apps. No need for virtual environments!

**Prerequisites:**
- Docker and Docker Compose installed

**Steps:**

1. **Navigate to the project directory:**
   ```bash
   cd news-search-engine
   ```

2. **Set up your NewsAPI key:**
   ```bash
   # On Windows:
   copy .env.example .env
   
   # On macOS/Linux:
   cp .env.example .env
   ```
   
3. **Edit the `.env` file** and add your API key from [NewsAPI.org](https://newsapi.org/register):
   ```
   NEWSAPI_KEY=your_actual_api_key_here
   ```

4. **Build and run with Docker:**
   ```bash
   docker-compose up --build
   ```

5. **To stop the container:**
   ```bash
   # Press Ctrl+C, then:
   docker-compose down
   ```

**Note:** 
- CSV output files will be saved in the `./output` directory on your host machine
- This runs the app in production mode (container starts and runs `main.py`)
- For development, use Option 2 (Dev Container) instead

## Usage

**With local venv (Option 1)**
```bash
# Make sure your virtual environment is activated first
python main.py
```

**Dev Container (Option 2):**
```bash
# Inside VS Code Dev Container terminal
python main.py
```

**With Docker Compose (Option 3):**
```bash
# From host machine
docker-compose up
```

### Using the Application

1. **Select Language**: Choose between English (1) or German (2)
2. **Enter Topic**: Type any topic you want to search for (e.g., "artificial intelligence", "climate change", "Olympics")
3. **View Results**: The application will display:
   - Top-15 articles with titles, URLs, publication dates, and sources
   - A CSV file with all matching articles (saved automatically)
   - An AI-generated summary of the top headlines
   - Named entities mentioned in headlines, sorted by frequency
4. **Continue or Exit**: Choose to search for another topic or exit

### Example Session

```
======================================================================
         Welcome to the News Search Engine
======================================================================

Select language:
  1. English (en)
  2. German (de)

Enter your choice (1 or 2) [default: 1]: 1

======================================================================

Enter a topic to search for (or 'quit' to exit): artificial intelligence

🔍 Searching for news about: 'artificial intelligence' (language: en)
Please wait...

✓ Found 87 articles

✓ CSV file saved: news_artificial_intelligence_en_20260119_143052.csv

======================================================================
TOP 15 ARTICLES (sorted by relevancy)
======================================================================

1. New AI Model Breaks Records in Language Understanding
   Source: Tech News Daily
   Published: 2026-01-18 14:23:00
   URL: https://example.com/ai-breakthrough

...
```


## Running Tests

To run the unit tests:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_csv_handler.py

# Run with coverage report
pytest --cov=src
```

## Output Files

CSV files are automatically generated with the following naming convention:
```
news_<query>_<language>_<timestamp>.csv
```

Each CSV file contains:
- Title
- URL
- Published Date
- Source
- Author
- Description

## API Limitations

The free tier of NewsAPI has the following limitations:
- 100 requests per day
- Maximum 100 articles per request
- Articles from the last 30 days
- Some news sources may be restricted

For higher limits, consider upgrading to a paid NewsAPI plan.

## Troubleshooting

### "NewsAPI key not found or not set"
- Make sure you've created a `.env` file in the project root
- Verify that your API key is correct and not set to `your_api_key_here`

### "spaCy model not found"
- Download the required language model: `python -m spacy download en_core_web_sm`
- For German: `python -m spacy download de_core_news_sm`

### "ModuleNotFoundError"
- Ensure your virtual environment is activated
- Run `pip install -r requirements.txt` again

### Slow summarization on first run
- The first time you run summarization, the BART model (about 1.6GB) will be downloaded
- Subsequent runs will be faster as the model is cached

## Technologies Used
pandas**: CSV data handling
- **Python-dotenv**: Environment variable management (12-factor app config)
- **Docker**: Containerization for consistent environments
- **NewsAPI**: News article retrieval
- **spaCy**: Named Entity Recognition
- **Transformers (BART)**: Text summarization
- **Python-dotenv**: Environment variable management
- **Pytest**: Unit testing

## License

This project is provided as-is for educational and evaluation purposes.

## Notes

- The summarization model requires an internet connection for the first download
- Large models may require significant disk space (~2GB)
- Processing time depends on the number of articles and your hardware
- Tested with Python 3.12.10 (last official 3.12 release with binary installers)
- Take-home assignment @ summetix