from datetime import datetime
from typing import List, Dict
from src.job_boards.linkedin_client import LinkedInClient
from src.parsers.resume_parser import ResumeAnalyzer
from src.utils.cover_letter_generator import CoverLetterGenerator
from src.config import Config

class JobHunter:
    def __init__(self):
        self.linkedin_client = LinkedInClient()
        self.resume_analyzer = ResumeAnalyzer(Config.RESUME_PATH)
        self.cover_letter_generator = CoverLetterGenerator()
        self.applied_jobs = []
    
    def hunt_jobs(self):
        """Main job hunting process"""
        print('Initializing job search on LinkedIn...')
        all_jobs = []
        
        # Search across all configured locations and keywords
        for location in Config.LOCATIONS:
            for keyword in Config.KEYWORDS:
                print(f'Searching for {keyword} in {location}...')
                try:
                    jobs = self.linkedin_client.search_jobs(keyword, location)
                    print(f'Found {len(jobs)} potential matches')
                    all_jobs.extend(jobs)
                except Exception as e:
                    print(f'Error searching LinkedIn for {keyword} in {location}: {str(e)}')
        
        print(f'Total jobs found: {len(all_jobs)}')
        
        # Filter and rank jobs
        relevant_jobs = self._filter_jobs(all_jobs)
        print(f'Relevant jobs after filtering: {len(relevant_jobs)}')
        
        ranked_jobs = self._rank_jobs(relevant_jobs)
        print('Jobs ranked by match score')
        
        # Apply to top ranked jobs
        for job in ranked_jobs[:Config.MAX_APPLICATIONS_PER_DAY]:
            if Config.AUTO_APPLY:
                self._apply_to_job(job)
            else:
                self._save_job_for_review(job)
    
    def _filter_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Filter jobs based on criteria"""
        filtered = []
        for job in jobs:
            # Skip if already applied
            if job['id'] in [j['id'] for j in self.applied_jobs]:
                continue
                
            # Check for required marketing leadership keywords
            leadership_keywords = ['head', 'director', 'vp', 'vice president', 'lead']
            marketing_keywords = ['marketing', 'growth', 'gtm', 'web3']
            
            title_lower = job['title'].lower()
            if any(k in title_lower for k in leadership_keywords) and \
               any(k in title_lower for k in marketing_keywords):
                filtered.append(job)
        
        return filtered
    
    def _rank_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Rank jobs based on match score"""
        for job in jobs:
            # Simple scoring for now
            score = 0
            title_lower = job['title'].lower()
            if 'web3' in title_lower or 'blockchain' in title_lower:
                score += 2
            if 'head' in title_lower or 'director' in title_lower:
                score += 1
            if 'marketing' in title_lower:
                score += 1
            job['match_score'] = score
        
        return sorted(jobs, key=lambda x: x['match_score'], reverse=True)
    
    def _apply_to_job(self, job: Dict):
        """Apply to a specific job"""
        print(f'\nPreparing application for: {job["title"]} at {job["company"]}')
        
        # Generate custom cover letter
        cover_letter = self.cover_letter_generator.generate(
            job_title=job['title'],
            company_name=job['company'],
            job_description=job.get('description', '')
        )
        
        print('Generated custom cover letter')
        
        # For now, just track the application
        self.applied_jobs.append({
            'id': job['id'],
            'title': job['title'],
            'company': job['company'],
            'date_applied': datetime.now().isoformat(),
            'status': 'ready_to_apply',
            'match_score': job['match_score'],
            'application_url': job['url']
        })
        
        print(f'Job saved: {job["url"]}')
    
    def _save_job_for_review(self, job: Dict):
        """Save job for manual review"""
        self.applied_jobs.append({
            'id': job['id'],
            'title': job['title'],
            'company': job['company'],
            'date_saved': datetime.now().isoformat(),
            'status': 'to_review',
            'match_score': job['match_score'],
            'application_url': job['url']
        })
        print(f'Saved job for review: {job["title"]} at {job["company"]}')
