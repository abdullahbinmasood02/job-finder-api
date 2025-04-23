# Job Finder API - Technical Documentation

## Introduction

The Job Finder API is a FastAPI-based service that fetches job listings from popular online job platforms including LinkedIn, Indeed, and Glassdoor. It uses advanced filtering techniques with OpenAI's GPT models to match jobs to user criteria, providing a streamlined way to find relevant positions across multiple job boards simultaneously.

## API Endpoints

### 1. POST /api/v1/jobs/search

This is the main endpoint that allows searching for jobs across multiple platforms based on detailed search criteria.

**Request Format:**

```json
{
  "position": "Full Stack Engineer",
  "experience": "2 years",
  "salary": "70,000 PKR to 120,000 PKR",
  "jobNature": "onsite",
  "location": "Peshawar, Pakistan",
  "skills": "full stack, MERN, Node.js, Express.js, React.js, Next.js, Firebase, TailwindCSS, CSS Frameworks, Tokens handling"
}
```

**Response Format:**

```json
{
  "relevant_jobs": [
    {
      "job_title": "Full Stack Engineer",
      "company": "XYZ Pvt Ltd",
      "experience": "2+ years",
      "jobNature": "onsite",
      "location": "Islamabad, Pakistan",
      "salary": "100,000 PKR",
      "apply_link": "https://linkedin.com/job123",
      "source": "LinkedIn"
    },
    {
      "job_title": "MERN Stack Developer",
      "company": "ABC Technologies",
      "experience": "2 years",
      "jobNature": "onsite",
      "location": "Lahore, Pakistan",
      "salary": "90,000 PKR",
      "apply_link": "https://indeed.com/job456",
      "source": "Indeed"
    }
  ]
}
```

### 2. GET /api/v1/jobs

Legacy endpoint that performs a simplified search using just query and location. This endpoint is useful for quick searches without specifying all criteria.

**Request Parameters:**
- `query`: Job title or keywords (required)
- `location`: Job location (optional)

**Example Request:**
```
GET /api/v1/jobs?query=javascript+developer&location=lahore
```

**Example Response:**
Same format as the POST endpoint

## Implementation Details

### Project Structure

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

### Architecture

The API follows a clean, modular architecture:

1. **API Layer**: Handles HTTP requests and responses
2. **Service Layer**: Manages the business logic
3. **Scraper Layer**: Handles web scraping from different sources
4. **Filtering Layer**: Processes and filters job listings for relevance

### 1. Job Scraping Layer

The API implements specialized scrapers for each job platform:

- **LinkedIn Scraper**: Uses Selenium to navigate LinkedIn's job search and extract listings
- **Indeed Scraper**: Extracts job listings from Indeed's search results
- **Glassdoor Scraper**: Handles Glassdoor's job listings (with mock data fallback)

Each scraper implements the BaseScraper abstract class, ensuring consistent interfaces across different job sources:

```python
class BaseScraper(ABC):
    @abstractmethod
    def fetch_jobs(self, query: str, location: str) -> List[Dict]:
        pass
    
    @abstractmethod
    def parse_jobs(self, content: Any) -> List[Dict]:
        pass
```

#### Scraping Techniques

- **Dynamic Content Handling**: Uses Selenium for JavaScript-rendered content
- **HTML Parsing**: BeautifulSoup for extracting data from HTML
- **User Agent Rotation**: Prevents detection and blocking
- **Headless Mode**: Allows running without visible browser windows
- **Wait Strategies**: Ensures content is loaded before extraction

### 2. Relevance Filtering

The API uses two approaches to filter jobs for relevance:

#### LLM-Based Filtering
When an OpenAI API key is available, the system uses GPT-3.5-turbo to evaluate each job against the search criteria. The prompt evaluates:

1. Job title match with requested position
2. Experience requirements
3. Location compatibility
4. Job nature (remote/onsite/hybrid)
5. Salary range match

Here's the LLM prompt structure:
```
Evaluate if the following job posting is relevant to the user's search criteria.

Search Criteria:
- Position: {position}
- Experience: {experience}
- Salary Range: {salary}
- Job Nature: {job_nature}
- Location: {location}
- Required Skills: {skills}

Job Posting:
- Job Title: {job_title}
- Company: {company}
- Experience Required: {job_experience}
- Job Nature: {job_job_nature}
- Location: {job_location}
- Salary: {job_salary}

Determine if this job is a good match for the search criteria considering the following:
1. Does the job title match or is it closely related to the position being sought?
2. Is the experience level appropriate?
3. Is the location compatible?
4. Is the job nature (remote/onsite/hybrid) compatible?
5. Is the salary within the expected range?

Answer only with 'YES' or 'NO'.
```

#### Basic Filtering
When no OpenAI API key is available, the system falls back to keyword-based matching:
- Checks if job title contains any keywords from the requested position
- Checks if job title contains any of the required skills

```python
def _basic_filtering(self, jobs: List[Dict], request: JobSearchRequest) -> List[Dict]:
    relevant_jobs = []
    position_keywords = set(request.position.lower().split())
    skills_keywords = set(skill.strip().lower() for skill in request.skills.split(','))
    
    for job in jobs:
        title = job["job_title"].lower()
        title_match = any(keyword in title for keyword in position_keywords)
        skills_match = any(skill in title for skill in skills_keywords)
        
        if title_match or skills_match:
            relevant_jobs.append(job)
    
    return relevant_jobs
```

## Security Considerations

- **API Key Protection**: Sensitive API keys are stored in environment variables
- **User Agent Rotation**: Makes detection of scraping activity more difficult
- **Rate Limiting**: Prevents overwhelming target websites
- **Headless Browser Mode**: Reduces fingerprinting
- **Error Handling**: Prevents leaking sensitive information in error messages
- **Input Validation**: All request data is validated using Pydantic models

## Performance Considerations

- **Concurrent Scraping**: Uses asyncio to scrape multiple sources simultaneously
- **Connection Pooling**: Reduces the overhead of creating new connections
- **Caching Strategies**: Future improvement to cache common searches
- **Resource Limitation**: Controls the number of concurrent browser instances
- **Mock Data Fallback**: Ensures the API returns data even if scraping fails

## Error Handling

The API implements comprehensive error handling:
- **Graceful Degradation**: When OpenAI API is unavailable, falls back to basic filtering
- **Scraping Fallbacks**: Uses mock data when scraping fails
- **Structured Error Responses**: Provides clear error messages
- **Detailed Logging**: Helps with debugging and monitoring
- **Exception Boundaries**: Prevents failures in one component from affecting others

## Future Enhancements

1. **Additional Job Sources**: Integration with more job platforms
2. **Advanced Filtering Options**: More granular search criteria
3. **User Preferences**: Save user search preferences
4. **Notification System**: Alert users of new matching jobs
5. **Performance Optimizations**: Caching and database storage for common searches

## How to Test

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env` file (follow `.env.example`):
   ```
   OPENAI_API_KEY=your_openai_api_key
   HEADLESS_BROWSER=True
   WAIT_TIME=10
   SECRET_KEY=your_secret_key
   DEBUG=True
   ```

3. Start the server:
   ```
   python -m uvicorn app.main:app --reload
   ```

4. Try a sample request using curl:
   ```
   curl -X POST "http://localhost:8000/api/v1/jobs/search" \
   -H "Content-Type: application/json" \
   -d '{
     "position": "Full Stack Engineer", 
     "experience": "2 years", 
     "salary": "70,000 PKR to 120,000 PKR", 
     "jobNature": "onsite", 
     "location": "Peshawar, Pakistan", 
     "skills": "full stack, MERN, Node.js, Express.js, React.js"
   }'
   ```
   
5. Or use the Swagger UI at `http://localhost:8000/docs`

## Conclusion

The Job Finder API provides a powerful and flexible solution for aggregating job listings from multiple sources and filtering them using advanced AI techniques. Its modular architecture allows for easy extension and maintenance, making it suitable for both personal use and integration into larger applications.
