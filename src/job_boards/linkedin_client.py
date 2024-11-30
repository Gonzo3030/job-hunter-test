import requests
from urllib.parse import urlencode
from ..config import Config

class LinkedInClient:
    def __init__(self):
        self.client_id = Config.LINKEDIN_CLIENT_ID
        self.client_secret = Config.LINKEDIN_CLIENT_SECRET
        self.access_token = None

    def search_jobs(self, keywords, location):
        """Search for jobs on LinkedIn"""
        print(f'Searching LinkedIn for {keywords} in {location}')
        
        # For now, just use LinkedIn's public API which doesn't require authentication
        base_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search'
        
        params = {
            'keywords': keywords,
            'location': location,
            'start': 0,
            'sortBy': 'R',  # Relevance
            'f_TPR': 'r86400',  # Past 24 hours
        }
        
        try:
            url = f'{base_url}?{urlencode(params)}'
            response = requests.get(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (compatible; JobBot/1.0)',
                }
            )
            
            if response.status_code == 200:
                return self._parse_jobs(response.text)
            else:
                print(f'Error searching LinkedIn: Status code {response.status_code}')
                return []
                
        except Exception as e:
            print(f'Error searching LinkedIn: {str(e)}')
            return []
    
    def _parse_jobs(self, html_content):
        """Parse LinkedIn jobs from HTML response"""
        from bs4 import BeautifulSoup
        
        jobs = []
        soup = BeautifulSoup(html_content, 'html.parser')
        
        job_cards = soup.find_all('div', {'class': 'job-search-card'})
        
        for card in job_cards:
            try:
                title = card.find('h3', {'class': 'base-search-card__title'}).text.strip()
                company = card.find('h4', {'class': 'base-search-card__subtitle'}).text.strip()
                location = card.find('span', {'class': 'job-search-card__location'}).text.strip()
                job_link = card.find('a', {'class': 'base-card__full-link'}).get('href')
                
                job_data = {
                    'id': job_link.split('?')[0].split('-')[-1],
                    'title': title,
                    'company': company,
                    'location': location,
                    'url': job_link,
                    'source': 'LinkedIn',
                    'description': self._get_job_description(job_link) if job_link else ''
                }
                
                jobs.append(job_data)
                print(f'Found job: {title} at {company}')
                
            except Exception as e:
                print(f'Error parsing job card: {str(e)}')
                continue
        
        return jobs
    
    def _get_job_description(self, job_url):
        """Get full job description from job detail page"""
        try:
            response = requests.get(
                job_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (compatible; JobBot/1.0)',
                }
            )
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                description_div = soup.find('div', {'class': 'description__text'})
                if description_div:
                    return description_div.text.strip()
            return ''
            
        except Exception as e:
            print(f'Error getting job description: {str(e)}')
            return ''
