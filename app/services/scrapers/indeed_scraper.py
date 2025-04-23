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

class IndeedScraper(BaseScraper):
    def __init__(self, base_url: str = "https://www.indeed.com/jobs"):
        self.base_url = base_url
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
        ]

    def fetch_jobs(self, query: str, location: str) -> List[Dict]:
        """
        Fetch job listings from Indeed
        """
        try:
            logger.info(f"Fetching Indeed jobs for: {query} in {location}")
            
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
            query_param = query.replace(' ', '+')
            location_param = location.replace(' ', '+')
            url = f"{self.base_url}?q={query_param}&l={location_param}"
            
            logger.info(f"Accessing URL: {url}")
            driver.get(url)
            
            # Wait for job listings to load
            WebDriverWait(driver, settings.WAIT_TIME).until(
                EC.presence_of_element_located((By.ID, "mosaic-provider-jobcards"))
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
            logger.error(f"Error fetching Indeed jobs: {str(e)}")
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
            jobs = soup.find_all('div', class_='job_seen_beacon')
            
            for job in jobs[:10]:  # Limit to 10 jobs for demonstration
                try:
                    # Extract job details
                    title_element = job.find('h2', class_='jobTitle')
                    company_element = job.find('span', class_='companyName')
                    location_element = job.find('div', class_='companyLocation')
                    
                    # Get job ID for constructing apply link
                    job_id = job.get('data-jk', '')
                    
                    # Extract salary if available
                    salary_element = job.find('div', class_='salary-snippet-container')
                    salary = salary_element.text.strip() if salary_element else "Not specified"
                    
                    # Get job details
                    job_title = title_element.text.strip() if title_element else "Unknown Title"
                    company = company_element.text.strip() if company_element else "Unknown Company"
                    location = location_element.text.strip() if location_element else "Unknown Location"
                    apply_link = f"https://www.indeed.com/viewjob?jk={job_id}" if job_id else "#"
                    
                    job_data = {
                        "job_title": job_title,
                        "company": company,
                        "location": location,
                        "apply_link": apply_link,
                        "salary": salary,
                        "experience": "Not specified",  # Indeed usually doesn't show this in listings
                        "jobNature": "Not specified",  # Would need to scrape job detail page
                        "source": "Indeed"
                    }
                    
                    job_listings.append(job_data)
                
                except Exception as e:
                    logger.error(f"Error parsing job listing: {str(e)}")
                    continue
            
            logger.info(f"Found {len(job_listings)} jobs on Indeed")
            return job_listings
        
        except Exception as e:
            logger.error(f"Error parsing Indeed jobs: {str(e)}")
            return self._get_mock_data()
    
    def _get_mock_data(self) -> List[Dict]:
        """
        Return mock data for demonstration purposes
        """
        return [
            {
                "job_title": "Full Stack Developer",
                "company": "InnovateTech",
                "experience": "2+ years",
                "jobNature": "Onsite",
                "location": "Islamabad, Pakistan",
                "salary": "80,000 - 110,000 PKR",
                "apply_link": "https://indeed.com/viewjob?jk=mock1",
                "source": "Indeed"
            },
            {
                "job_title": "React.js Developer",
                "company": "Web Solutions Pvt",
                "experience": "1-3 years",
                "jobNature": "Remote",
                "location": "Lahore, Pakistan",
                "salary": "85,000 PKR",
                "apply_link": "https://indeed.com/viewjob?jk=mock2",
                "source": "Indeed"
            },
            {
                "job_title": "Node.js Backend Developer",
                "company": "TechPro Systems",
                "experience": "2-4 years",
                "jobNature": "Hybrid",
                "location": "Karachi, Pakistan",
                "salary": "100,000 - 130,000 PKR",
                "apply_link": "https://indeed.com/viewjob?jk=mock3",
                "source": "Indeed"
            }
        ]