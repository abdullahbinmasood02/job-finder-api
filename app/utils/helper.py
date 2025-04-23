def format_job_data(job):
    return {
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "description": job.description,
        "url": job.url,
        "date_posted": job.date_posted
    }

def validate_search_params(params):
    if not params.get("keywords"):
        raise ValueError("Keywords are required for job search.")
    if not params.get("location"):
        raise ValueError("Location is required for job search.")
    return True

def extract_job_listings(raw_data):
    job_listings = []
    for item in raw_data:
        job = format_job_data(item)
        job_listings.append(job)
    return job_listings