from app.services.scrapers.linkedin_scraper import LinkedInScraper
from app.services.scrapers.indeed_scraper import IndeedScraper
from app.services.scrapers.glassdoor_scraper import GlassdoorScraper
import pytest

@pytest.fixture
def linkedin_scraper():
    return LinkedInScraper()

@pytest.fixture
def indeed_scraper():
    return IndeedScraper()

@pytest.fixture
def glassdoor_scraper():
    return GlassdoorScraper()

def test_linkedin_scraper_fetches_jobs(linkedin_scraper):
    jobs = linkedin_scraper.fetch_jobs("Software Engineer", "Remote")
    assert isinstance(jobs, list)
    assert len(jobs) > 0
    assert all("title" in job for job in jobs)

def test_indeed_scraper_fetches_jobs(indeed_scraper):
    jobs = indeed_scraper.fetch_jobs("Data Scientist", "New York")
    assert isinstance(jobs, list)
    assert len(jobs) > 0
    assert all("title" in job for job in jobs)

def test_glassdoor_scraper_fetches_jobs(glassdoor_scraper):
    jobs = glassdoor_scraper.fetch_jobs("Product Manager", "San Francisco")
    assert isinstance(jobs, list)
    assert len(jobs) > 0
    assert all("title" in job for job in jobs)