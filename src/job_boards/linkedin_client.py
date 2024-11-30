from linkedin import linkedin
from ..config import Config

class LinkedInClient:
    def __init__(self):
        self.application = linkedin.LinkedInApplication(
            token=Config.LINKEDIN_CLIENT_ID
        )
    
    def search_jobs(self, keywords, location):
        """Search for jobs on LinkedIn"""
        jobs = self.application.search_job(
            params={
                'keywords': keywords,
                'location': location,
                'experience-level': ['executive', 'director'],
                'f_TP': ['1', '2'],  # Past day, Past week
                'position': ['Marketing', 'Growth', 'Business Development']
            }
        )
        return self._parse_jobs(jobs)
    
    def _parse_jobs(self, jobs_data):
        """Parse LinkedIn job data into standard format"""
        parsed_jobs = []
        for job in jobs_data.get('elements', []):
            parsed_jobs.append({
                'id': job.get('id'),
                'title': job.get('title'),
                'company': job.get('company'),
                'location': job.get('location'),
                'description': job.get('description'),
                'url': job.get('url'),
                'source': 'LinkedIn'
            })
        return parsed_jobs
