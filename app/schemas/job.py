from pydantic import BaseModel, Field
from typing import List, Optional

class Job(BaseModel):
    title: str
    company: str
    location: str
    description: str
    url: str
    date_posted: Optional[str] = None

class JobListResponse(BaseModel):
    jobs: List[Job]

class JobSearchRequest(BaseModel):
    position: str
    experience: str
    salary: Optional[str] = None
    jobNature: Optional[str] = None
    location: Optional[str] = None
    skills: str

    class Config:
        schema_extra = {
            "example": {
                "position": "Full Stack Engineer",
                "experience": "2 years",
                "salary": "70,000 PKR to 120,000 PKR",
                "jobNature": "onsite",
                "location": "Peshawar, Pakistan",
                "skills": "full stack, MERN, Node.js, Express.js, React.js, Next.js, Firebase, TailwindCSS, CSS Frameworks, Tokens handling"
            }
        }

class JobResponse(BaseModel):
    job_title: str
    company: str
    experience: str
    jobNature: str
    location: str
    salary: str
    apply_link: str
    source: str = Field(description="Source platform (LinkedIn, Indeed, etc.)")

class JobSearchResponse(BaseModel):
    relevant_jobs: List[JobResponse]
    
    class Config:
        schema_extra = {
            "example": {
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
        }