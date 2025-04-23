from pydantic import BaseModel
from typing import Optional

class Job(BaseModel):
    title: str
    company: str
    location: str
    description: Optional[str] = None
    url: str
    source: str
    date_posted: Optional[str] = None
    salary: Optional[str] = None