import requests
from ..config import Config

class LinkedInClient:
    def __init__(self):
        self.client_id = Config.LINKEDIN_CLIENT_ID
        self.client_secret = Config.LINKEDIN_CLIENT_SECRET
        self.access_token = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with LinkedIn"""
        auth_url = 'https://www.linkedin.com/oauth/v2/accessToken'
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        response = requests.post(auth_url, data=data)
        if response.status_code == 200:
            self.access_token = response.json()['access_token']
        else:
            raise Exception(f'LinkedIn authentication failed: {response.text}')
    
    def search_jobs(self, keywords, location):
        """Search for jobs on LinkedIn"""
        print(f'Searching LinkedIn for {keywords} in {location}')
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
        }
        
        # Using LinkedIn's Job Search API
        url = 'https://api.linkedin.com/v2/jobSearch'
        params = {
            'keywords': keywords,
            'location': location,
            'count': 20
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                jobs = response.json().get('elements', [])
                return self._parse_jobs(jobs)
            else:
                print(f'LinkedIn API error: {response.status_code} - {response.text}')
                return []
        except Exception as e:
            print(f'Error searching LinkedIn: {str(e)}')
            return []
    
    def _parse_jobs(self, jobs_data):
        """Parse LinkedIn job data into standard format"""
        parsed_jobs = []
        for job in jobs_data:
            parsed_jobs.append({
                'id': job.get('id'),
                'title': job.get('title', ''),
                'company': job.get('company', {}).get('name', ''),
                'location': job.get('location', ''),
                'description': job.get('description', ''),
                'url': job.get('applyUrl', ''),
                'source': 'LinkedIn'
            })
        return parsed_jobs
