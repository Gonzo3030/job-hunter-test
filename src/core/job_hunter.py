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
        print('Initializing job search on LinkedIn...\n')
        all_jobs = []
        
        # Search and process jobs in batches by location
        for location in Config.LOCATIONS:
            location_jobs = []
            print(f'Searching in {location}...')
            
            for keyword in Config.KEYWORDS:
                print(f'\nSearching for {keyword}...')
                try:
                    jobs = self.linkedin_client.search_jobs(keyword, location)
                    print(f'Found {len(jobs)} potential matches')
                    location_jobs.extend(jobs)
                except Exception as e:
                    print(f'Error searching LinkedIn: {str(e)}')
            
            # Process this location's jobs before moving to next location
            print(f'\nProcessing {len(location_jobs)} jobs found in {location}...')
            relevant_jobs = self._filter_jobs(location_jobs)
            print(f'Relevant jobs after filtering: {len(relevant_jobs)}\n')
            
            if relevant_jobs:
                ranked_jobs = self._rank_jobs(relevant_jobs)
                print('Top matches for this location:')
                for job in ranked_jobs[:5]:
                    print(f"- {job['title']} at {job['company']} (Score: {job['match_score']})")
                
                all_jobs.extend(relevant_jobs)
                
                # Process top 3 jobs from this location
                for job in ranked_jobs[:3]:
                    if Config.AUTO_APPLY:
                        self._apply_to_job(job)
                    else:
                        self._save_job_for_review(job)
                        
            print('\n' + '-'*50 + '\n')
        
        print(f'\nSearch complete! Found {len(all_jobs)} total relevant jobs')
        
    def _filter_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Filter jobs based on criteria"""
        filtered = []
        for job in jobs:
            # Skip if already applied
            if job['id'] in [j['id'] for j in self.applied_jobs]:
                continue
            
            title_lower = job['title'].lower()
            company_lower = job['company'].lower()
            
            # Skip if contains exclude terms
            if any(term in title_lower for term in Config.EXCLUDE_TERMS):
                continue
            
            # Check if it's a leadership role
            is_leadership = any([
                'head' in title_lower,
                'director' in title_lower,
                'vp' in title_lower,
                'vice president' in title_lower,
                'lead' in title_lower and ('marketing' in title_lower or 'growth' in title_lower),
                'chief' in title_lower
            ])
            
            # Check if it's a relevant role
            is_relevant_role = any([
                'marketing' in title_lower,
                'growth' in title_lower,
                'partnerships' in title_lower,
                'business development' in title_lower,
                'bd' in title_lower and ('head' in title_lower or 'director' in title_lower)
            ])
            
            if is_leadership and is_relevant_role:
                filtered.append(job)
                print(f'Matched Job: {job["title"]} at {job["company"]}')
        
        return filtered
    
    def _rank_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Rank jobs based on match score"""
        for job in jobs:
            score = 0
            title_lower = job['title'].lower()
            company_lower = job['company'].lower()
            
            # Priority for Web3/Blockchain
            if any(term in title_lower or term in company_lower 
                   for term in ['web3', 'blockchain', 'crypto', 'defi']):
                score += 3
                
            # Priority for remote roles
            if 'remote' in job['location'].lower():
                score += 2
                
            # Leadership level
            if 'head' in title_lower or 'chief' in title_lower:
                score += 2
            elif 'director' in title_lower or 'vp' in title_lower:
                score += 1
                
            # Role type
            if 'marketing' in title_lower:
                score += 1
            if 'growth' in title_lower:
                score += 1
            if 'partnerships' in title_lower or 'business development' in title_lower:
                score += 1
                
            # Target industries
            if any(industry in company_lower for industry in Config.TARGET_INDUSTRIES):
                score += 1
                
            job['match_score'] = score
        
        return sorted(jobs, key=lambda x: x['match_score'], reverse=True)
    
    def _apply_to_job(self, job: Dict):
        """Apply to a specific job"""
        print(f'\nPreparing application for: {job["title"]} at {job["company"]}')
        print(f'Match Score: {job["match_score"]}')
        
        # Generate custom cover letter
        cover_letter = self.cover_letter_generator.generate(
            job_title=job['title'],
            company_name=job['company'],
            job_description=job.get('description', '')
        )
        
        print('Generated custom cover letter')
        
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
