import requests
from urllib.parse import urlencode
from time import sleep
from bs4 import BeautifulSoup
from src.config import Config

class LinkedInClient:
    def __init__(self):
        self.client_id = Config.LINKEDIN_CLIENT_ID
        self.client_secret = Config.LINKEDIN_CLIENT_SECRET
        self.access_token = None
        self.retry_delay = 60  # seconds to wait after rate limit

    def search_jobs(self, keywords, location):
        """Search for jobs on LinkedIn"""
        print(f'Searching LinkedIn for {keywords} in {location}')
        
        base_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search'
        
        params = {
            'keywords': keywords,
            'location': location,
            'start': 0,
            'sortBy': 'R',
            'f_TPR': 'r86400',  # Last 24 hours
            'position': 1,
            'pageNum': 0,
            'f_WT': 2,  # Remote jobs included
        }
        
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                url = f'{base_url}?{urlencode(params)}'
                response = requests.get(
                    url,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                    }
                )
                
                if response.status_code == 200:
                    return self._parse_jobs(response.text)
                elif response.status_code == 429:  # Rate limit
                    print(f'Rate limited. Waiting {self.retry_delay} seconds...')
                    sleep(self.retry_delay)
                    self.retry_delay *= 2  # Exponential backoff
                    retry_count += 1
                    continue
                else:
                    print(f'Error searching LinkedIn: Status code {response.status_code}')
                    return []
                    
            except Exception as e:
                print(f'Error searching LinkedIn: {str(e)}')
                return []
        
        print('Max retries reached for this search')
        return []
    
    def _parse_jobs(self, html_content):
        """Parse LinkedIn jobs from HTML response"""
        jobs = []
        soup = BeautifulSoup(html_content, 'html.parser')
        
        job_cards = soup.find_all('div', {'class': 'job-search-card'})
        
        for card in job_cards:
            try:
                title_elem = card.find('h3', {'class': 'base-search-card__title'})
                company_elem = card.find('h4', {'class': 'base-search-card__subtitle'})
                location_elem = card.find('span', {'class': 'job-search-card__location'})
                link_elem = card.find('a', {'class': 'base-card__full-link'})
                
                if not all([title_elem, company_elem, location_elem, link_elem]):
                    continue
                
                title = title_elem.text.strip()
                company = company_elem.text.strip()
                location = location_elem.text.strip()
                job_link = link_elem.get('href')
                
                # Wait between job description requests to avoid rate limiting
                sleep(2)
                
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
            # Wait a bit before requesting job details
            sleep(1)
            
            response = requests.get(
                job_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
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