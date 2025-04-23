import asyncio
import logging
from typing import List, Dict

from app.schemas.job import JobSearchRequest, JobResponse
from app.services.scrapers.linkedin_scraper import LinkedInScraper
from app.services.scrapers.indeed_scraper import IndeedScraper
from app.services.scrapers.glassdoor_scraper import GlassdoorScraper
from app.services.relevance_filter import RelevanceFilter

logger = logging.getLogger(__name__)

class JobService:
    """
    Service for finding jobs across multiple platforms
    """
    
    def __init__(self):
        self.linkedin_scraper = LinkedInScraper()
        self.indeed_scraper = IndeedScraper()
        self.glassdoor_scraper = GlassdoorScraper()
        self.relevance_filter = RelevanceFilter()
    
    async def find_jobs(self, request: JobSearchRequest) -> List[Dict]:
        """
        Find jobs matching search criteria
        
        Args:
            request: Job search criteria
            
        Returns:
            List of relevant jobs
        """
        logger.info(f"Searching for jobs: {request.position}")
        
        try:
            # Extract search parameters
            query = request.position
            location = request.location if request.location else ""
            
            # Fetch jobs from all sources concurrently
            tasks = [
                self._fetch_linkedin_jobs(query, location),
                self._fetch_indeed_jobs(query, location),
                self._fetch_glassdoor_jobs(query, location)
            ]
            
            # Gather results
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results and handle exceptions
            all_jobs = []
            for result in results:
                if isinstance(result, Exception):
                    logger.error(f"Error fetching jobs: {result}")
                else:
                    all_jobs.extend(result)
            
            # Filter jobs for relevance
            relevant_jobs = self.relevance_filter.filter_jobs(all_jobs, request)
            
            logger.info(f"Found {len(relevant_jobs)} relevant jobs out of {len(all_jobs)} total jobs")
            return relevant_jobs
            
        except Exception as e:
            logger.error(f"Error in find_jobs: {str(e)}")
            raise
    
    async def _fetch_linkedin_jobs(self, query: str, location: str) -> List[Dict]:
        """
        Fetch jobs from LinkedIn
        """
        try:
            return self.linkedin_scraper.fetch_jobs(query, location)
        except Exception as e:
            logger.error(f"Error fetching LinkedIn jobs: {str(e)}")
            return []
    
    async def _fetch_indeed_jobs(self, query: str, location: str) -> List[Dict]:
        """
        Fetch jobs from Indeed
        """
        try:
            return self.indeed_scraper.fetch_jobs(query, location)
        except Exception as e:
            logger.error(f"Error fetching Indeed jobs: {str(e)}")
            return []
    
    async def _fetch_glassdoor_jobs(self, query: str, location: str) -> List[Dict]:
        """
        Fetch jobs from Glassdoor
        """
        try:
            return self.glassdoor_scraper.fetch_jobs(query, location)
        except Exception as e:
            logger.error(f"Error fetching Glassdoor jobs: {str(e)}")
            return []