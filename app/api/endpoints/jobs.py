from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict

from app.schemas.job import JobSearchRequest, JobSearchResponse
from app.services.job_service import JobService

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
    responses={404: {"description": "Not found"}},
)

@router.post("/search", response_model=JobSearchResponse, summary="Search for jobs")
async def search_jobs(request: JobSearchRequest):
    """
    Search for jobs across multiple platforms based on the provided criteria.
    
    This endpoint scrapes job listings from LinkedIn, Indeed, and Glassdoor,
    then uses LLM to filter the results for relevance to the search criteria.
    
    ## Parameters:
    - **position**: Job title or position
    - **experience**: Years of experience required
    - **salary** (optional): Expected salary range
    - **jobNature** (optional): Type of job (onsite, remote, hybrid)
    - **location** (optional): Job location
    - **skills**: Required skills separated by commas
    
    ## Returns:
    A list of relevant job listings with details
    """
    try:
        job_service = JobService()
        relevant_jobs = await job_service.find_jobs(request)
        return JobSearchResponse(relevant_jobs=relevant_jobs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching for jobs: {str(e)}")

@router.get("/", response_model=JobSearchResponse)
async def get_jobs(query: str, location: str = None):
    """
    Legacy endpoint for fetching jobs based on query and location.
    Use POST /search for more advanced filtering.
    """
    try:
        # Create a simplified request
        request = JobSearchRequest(
            position=query,
            experience="",
            location=location,
            skills=query
        )
        # Create a service instance here instead of using global variable
        job_service = JobService()
        relevant_jobs = await job_service.find_jobs(request)
        return JobSearchResponse(relevant_jobs=relevant_jobs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))