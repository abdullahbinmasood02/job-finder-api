# Job Finder API

A FastAPI-powered API that fetches relevant job listings from LinkedIn, Indeed, and Glassdoor based on user criteria. The API uses OpenAI's GPT model to analyze and filter jobs for relevance.

## 🌟 Features

- **Multi-Platform Support**: Fetches jobs from LinkedIn, Indeed, and Glassdoor
- **Advanced Relevance Filtering**: Uses OpenAI GPT to match jobs with search criteria
- **Flexible Search**: Filter by position, experience, salary, location, and skills
- **Robust Web Scraping**: Uses Selenium and BeautifulSoup for reliable data extraction
- **Fast Performance**: Concurrent scraping with asyncio for quick results
- **Fallback Mechanisms**: Basic filtering when LLM is unavailable, mock data when scraping fails

## 🔧 Technologies Used

- **FastAPI**: Modern, fast API framework
- **Selenium & BeautifulSoup**: Web scraping tools
- **OpenAI API**: For intelligent job matching
- **Async IO**: For concurrent operations

## 🏗️ Project Structure

```
job-finder-api/
├── app/
│   ├── api/                  # API routes and endpoints
│   ├── core/                 # Core configurations
│   ├── models/               # Data models
│   ├── schemas/              # Pydantic schemas for validation
│   ├── services/             # Business logic
│   │   ├── scrapers/         # Web scrapers for job platforms
│   ├── utils/                # Utility functions
│   └── main.py               # FastAPI application entry point
├── tests/                    # Test suite
├── docs/                     # Documentation
├── examples/                 # Sample request/response files
├── .env.example              # Environment variables example
└── requirements.txt          # Project dependencies
```

## 📋 Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd job-finder-api
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example` and add your API keys

## 🚀 Usage

1. Start the API server:
   ```
   python -m uvicorn app.main:app --reload
   ```

2. Access the API documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

3. Send a request:
   ```bash
   curl -X POST "http://localhost:8000/api/v1/jobs/search" \
   -H "Content-Type: application/json" \
   -d @examples/request.json
   ```

## 📊 API Endpoints

### POST /api/v1/jobs/search
Search for jobs across multiple platforms with detailed criteria.

### GET /api/v1/jobs
Simple job search with basic query and location.

## 📄 Documentation

For detailed documentation, see the [docs folder](./docs/Documentation.md).

## 🧪 Testing

Run the test suite:
```
pytest
```

## 📝 License

This project is licensed under the MIT License.