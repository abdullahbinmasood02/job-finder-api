import os
import logging
from typing import List, Dict
import openai

from app.core.config import settings
from app.schemas.job import JobSearchRequest

logger = logging.getLogger(__name__)

class RelevanceFilter:
    """
    Filter jobs for relevance based on user search criteria using LLM
    """
    
    def __init__(self):
        self.openai_api_key = settings.OPENAI_API_KEY
        
        if not self.openai_api_key:
            logger.warning("OpenAI API key not found. Relevance filtering will be limited.")
            self.use_openai = False
        else:
            self.use_openai = True
            openai.api_key = self.openai_api_key
    
    def filter_jobs(self, jobs: List[Dict], request: JobSearchRequest) -> List[Dict]:
        """
        Filter jobs based on relevance to search criteria
        
        Args:
            jobs: List of job dictionaries
            request: Job search request
            
        Returns:
            List of relevant job dictionaries
        """
        if not jobs:
            return []
        
        logger.info(f"Filtering {len(jobs)} jobs for relevance")
        
        try:
            # If OpenAI API key is not available, use basic filtering
            if not self.use_openai:
                return self._basic_filtering(jobs, request)
            
            # Use LLM for relevance filtering
            relevant_jobs = []
            
            for job in jobs:
                if self._is_job_relevant_llm(job, request):
                    relevant_jobs.append(job)
            
            logger.info(f"Found {len(relevant_jobs)} relevant jobs out of {len(jobs)}")
            return relevant_jobs
        
        except Exception as e:
            logger.error(f"Error filtering jobs for relevance: {str(e)}")
            # Return all jobs if filtering fails
            return jobs
    
    def _is_job_relevant_llm(self, job: Dict, request: JobSearchRequest) -> bool:
        """
        Use OpenAI to determine if a job is relevant to the search criteria
        
        Args:
            job: Job dictionary
            request: Job search request
            
        Returns:
            True if job is relevant, False otherwise
        """
        try:
            # Create the prompt directly without using LangChain's PromptTemplate
            prompt = f"""
            Evaluate if the following job posting is relevant to the user's search criteria.
            
            Search Criteria:
            - Position: {request.position}
            - Experience: {request.experience}
            - Salary Range: {request.salary if request.salary else "Not specified"}
            - Job Nature: {request.jobNature if request.jobNature else "Not specified"}
            - Location: {request.location if request.location else "Not specified"}
            - Required Skills: {request.skills}
            
            Job Posting:
            - Job Title: {job["job_title"]}
            - Company: {job["company"]}
            - Experience Required: {job["experience"]}
            - Job Nature: {job["jobNature"]}
            - Location: {job["location"]}
            - Salary: {job["salary"]}
            
            Determine if this job is a good match for the search criteria. Consider the following:
            1. Does the job title match or is closely related to the position being sought?
            2. Is the experience level appropriate?
            3. Is the location compatible?
            4. Is the job nature (remote/onsite/hybrid) compatible?
            5. Is the salary within the expected range?
            
            Answer only with 'YES' or 'NO'.
            """
            
            # Get response from OpenAI
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a job matching AI assistant. You evaluate if jobs match search criteria."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=10,
                temperature=0.1,
            )
            
            answer = response.choices[0].message.content.strip().upper()
            is_relevant = answer == "YES"
            
            logger.debug(f"Job relevance for '{job['job_title']}': {is_relevant}")
            return is_relevant
            
        except Exception as e:
            logger.error(f"Error determining job relevance with LLM: {str(e)}")
            # Default to including the job if there's an error
            return True
    
    def _basic_filtering(self, jobs: List[Dict], request: JobSearchRequest) -> List[Dict]:
        """
        Basic filtering without using LLM
        
        Args:
            jobs: List of job dictionaries
            request: Job search request
            
        Returns:
            List of relevant job dictionaries
        """
        logger.info("Using basic filtering (no LLM)")
        relevant_jobs = []
        
        position_keywords = set(request.position.lower().split())
        skills_keywords = set(skill.strip().lower() for skill in request.skills.split(','))
        
        for job in jobs:
            title = job["job_title"].lower()
            
            # Check if title matches position
            title_match = any(keyword in title for keyword in position_keywords)
            
            # Check if title matches any skills
            skills_match = any(skill in title for skill in skills_keywords)
            
            # Simple relevance: title matches position or skills
            if title_match or skills_match:
                relevant_jobs.append(job)
        
        return relevant_jobs