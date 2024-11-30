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
        self.base_delay = 30  # Start with 30 seconds
        self.max_delay = 120  # Never wait more than 2 minutes

    def search_jobs(self, keywords, location):
        """Search for jobs on LinkedIn"""
        print(f'Searching LinkedIn for {keywords} in {location}')
        
        base_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search'
        
        params = {
            'keywords': keywords,
            'location': location,
            'start': 0,
            'sortBy': 'R',  # Relevance
            'f_TPR': 'r86400',  # Past 24 hours
            'f_WT': 2,  # Remote jobs included
        }
        
        max_retries = 3
        retry_count = 0
        current_delay = self.base_delay
        
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
                    print(f'Rate limited. Waiting {current_delay} seconds...')
                    sleep(current_delay)
                    # Increase delay for next time, but don't exceed max
                    current_delay = min(current_delay * 1.5, self.max_delay)
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
                
                # Skip job description fetch to avoid rate limiting
                job_data = {
                    'id': job_link.split('?')[0].split('-')[-1],
                    'title': title,
                    'company': company,
                    'location': location,
                    'url': job_link,
                    'source': 'LinkedIn',
                    'description': ''  # Skip description for now
                }
                
                jobs.append(job_data)
                print(f'Found job: {title} at {company}')
                
            except Exception as e:
                print(f'Error parsing job card: {str(e)}')
                continue
        
        return jobs