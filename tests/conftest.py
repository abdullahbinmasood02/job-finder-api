import pytest

@pytest.fixture
def sample_job_data():
    return {
        "title": "Software Engineer",
        "company": "Tech Company",
        "location": "Remote",
        "description": "Develop and maintain software applications.",
        "url": "https://example.com/job/software-engineer"
    }