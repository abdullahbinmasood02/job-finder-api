from abc import ABC, abstractmethod
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """Base class for all job source scrapers"""
    
    def __init__(self, source_name=None):
        self.source_name = source_name or "Unknown"

    @abstractmethod
    def fetch_jobs(self, query: str, location: str) -> List[Dict]:
        """
        Fetch job listings from source
        
        Args:
            query: Job title or keywords
            location: Job location
            
        Returns:
            List of job dictionaries
        """
        pass
    
    @abstractmethod
    def parse_jobs(self, content: Any) -> List[Dict]:
        """
        Parse the content and extract job listings
        
        Args:
            content: The content to parse (HTML, JSON, etc.)
            
        Returns:
            List of job dictionaries
        """
        pass
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Text to clean
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        text = text.strip()
        text = " ".join(text.split())  # Remove extra whitespace
        
        return text
    
    def format_salary(self, salary: str) -> str:
        """
        Format salary string
        
        Args:
            salary: Salary text
            
        Returns:
            Formatted salary
        """
        if not salary:
            return "Not specified"
            
        return self.clean_text(salary)

    def get_source_name(self):
        return self.source_name