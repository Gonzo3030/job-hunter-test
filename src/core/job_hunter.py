from typing import List, Dict
from ..job_boards.linkedin_client import LinkedInClient
from ..parsers.resume_parser import ResumeAnalyzer
from ..utils.cover_letter_generator import CoverLetterGenerator
from ..config import Config

class JobHunter:
    def __init__(self):
        self.linkedin_client = LinkedInClient()
        self.resume_analyzer = ResumeAnalyzer(Config.RESUME_PATH)
        self.cover_letter_generator = CoverLetterGenerator()
        self.applied_jobs = []
    
    def hunt_jobs(self):
        """Main job hunting process"""
        all_jobs = []
        
        # Search across all configured locations and keywords
        for location in Config.LOCATIONS:
            for keyword in Config.KEYWORDS:
                jobs = self.linkedin_client.search_jobs(keyword, location)
                all_jobs.extend(jobs)
        
        # Filter and rank jobs
        relevant_jobs = self._filter_jobs(all_jobs)
        ranked_jobs = self._rank_jobs(relevant_jobs)
        
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
            match_score = self.resume_analyzer.get_job_match_score(job['description'])
            job['match_score'] = match_score
        
        return sorted(jobs, key=lambda x: x['match_score'], reverse=True)
    
    def _apply_to_job(self, job: Dict):
        """Apply to a specific job"""
        # Generate custom cover letter
        cover_letter = self.cover_letter_generator.generate(
            job_title=job['title'],
            company_name=job['company'],
            job_description=job['description']
        )
        
        # TODO: Implement actual application submission
        # For now, just track the application
        self.applied_jobs.append({
            'id': job['id'],
            'title': job['title'],
            'company': job['company'],
            'date_applied': datetime.now(),
            'status': 'applied'
        })
    
    def _save_job_for_review(self, job: Dict):
        """Save job for manual review"""
        # TODO: Implement saving to database or file
        pass