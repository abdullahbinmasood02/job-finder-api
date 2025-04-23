import requests
import logging
from typing import List, Dict
from bs4 import BeautifulSoup
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from app.core.config import settings
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class LinkedInScraper(BaseScraper):
    def __init__(self, base_url: str = "https://www.linkedin.com/jobs/search"):
        self.base_url = base_url
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
        ]

    def fetch_jobs(self, query: str, location: str) -> List[Dict]:
        """
        Fetch job listings from LinkedIn using Selenium (to bypass restrictions)
        """
        try:
            logger.info(f"Fetching LinkedIn jobs for: {query} in {location}")
            
            # Set up Chrome options
            chrome_options = Options()
            if settings.HEADLESS_BROWSER:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument(f"user-agent={random.choice(self.user_agents)}")
            
            # Create a new Chrome driver
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            
            # Format the URL
            query_param = query.replace(' ', '%20')
            location_param = location.replace(' ', '%20')
            url = f"{self.base_url}?keywords={query_param}&location={location_param}"
            
            logger.info(f"Accessing URL: {url}")
            driver.get(url)
            
            # Wait for job listings to load
            WebDriverWait(driver, settings.WAIT_TIME).until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobs-search__results-list"))
            )
            
            # Let the page fully load
            time.sleep(3)
            
            # Get the page source and parse it
            html = driver.page_source
            
            # Close the driver
            driver.quit()
            
            # Parse the HTML to extract job listings
            return self.parse_jobs(html)
        
        except Exception as e:
            logger.error(f"Error fetching LinkedIn jobs: {str(e)}")
            # Return mock data for demonstration
            return self._get_mock_data()
    
    def parse_jobs(self, html: str) -> List[Dict]:
        """
        Parse HTML to extract job listings
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')
            job_listings = []
            
            # Find all job cards
            jobs = soup.find_all('div', class_='job-search-card')
            
            for job in jobs[:10]:  # Limit to 10 jobs for demonstration
                try:
                    # Extract job details
                    title_element = job.find('h3', class_='base-search-card__title')
                    company_element = job.find('h4', class_='base-search-card__subtitle')
                    location_element = job.find('span', class_='job-search-card__location')
                    link_element = job.find('a', class_='base-card__full-link')
                    
                    # Get job details
                    job_title = title_element.text.strip() if title_element else "Unknown Title"
                    company = company_element.text.strip() if company_element else "Unknown Company"
                    location = location_element.text.strip() if location_element else "Unknown Location"
                    link = link_element['href'] if link_element else "#"
                    
                    # LinkedIn typically doesn't show salary directly, 
                    # we could scrape individual job pages for more info
                    
                    job_data = {
                        "job_title": job_title,
                        "company": company,
                        "location": location,
                        "apply_link": link,
                        "salary": "Not specified",  # LinkedIn often doesn't show salary in listings
                        "experience": "Not specified",  # Would need to scrape job detail page
                        "jobNature": "Not specified",  # Would need to scrape job detail page
                        "source": "LinkedIn"
                    }
                    
                    job_listings.append(job_data)
                
                except Exception as e:
                    logger.error(f"Error parsing job listing: {str(e)}")
                    continue
            
            logger.info(f"Found {len(job_listings)} jobs on LinkedIn")
            return job_listings
        
        except Exception as e:
            logger.error(f"Error parsing LinkedIn jobs: {str(e)}")
            return self._get_mock_data()
    
    def _get_mock_data(self) -> List[Dict]:
        """
        Return mock data for demonstration purposes
        """
        return [
            {
                "job_title": "Full Stack Developer",
                "company": "TechCorp Ltd",
                "experience": "2-3 years",
                "jobNature": "Onsite",
                "location": "Islamabad, Pakistan",
                "salary": "90,000 - 120,000 PKR",
                "apply_link": "https://linkedin.com/jobs/view/mock1",
                "source": "LinkedIn"
            },
            {
                "job_title": "MERN Stack Engineer",
                "company": "Digital Solutions",
                "experience": "2+ years",
                "jobNature": "Hybrid",
                "location": "Lahore, Pakistan",
                "salary": "100,000 PKR",
                "apply_link": "https://linkedin.com/jobs/view/mock2",
                "source": "LinkedIn"
            },
            {
                "job_title": "Senior JavaScript Developer",
                "company": "WebApps Inc",
                "experience": "3+ years",
                "jobNature": "Remote",
                "location": "Karachi, Pakistan",
                "salary": "120,000 - 150,000 PKR",
                "apply_link": "https://linkedin.com/jobs/view/mock3",
                "source": "LinkedIn"
            }
        ]
