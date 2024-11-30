from typing import Dict

class ResumeAnalyzer:
    def __init__(self, resume_path: str):
        self.resume_path = resume_path
        self.skills = {
            'technical': ['Web3', 'Blockchain', 'SEO', 'SEM', 'Analytics'],
            'marketing': ['GTM', 'Growth Marketing', 'Content Marketing', 'B2B Marketing'],
            'leadership': ['Team Management', 'Strategy', 'Business Development']
        }
        
        self.experience_highlights = [
            'Led marketing initiatives resulting in $150M+ in bug bounties',
            'Achieved 2000% Y/Y growth in revenue',
            'Built and led teams of up to 6 marketers'
        ]
    
    def get_job_match_score(self, job_description: str) -> float:
        """Calculate match score between resume and job description"""
        if not job_description:
            return 0.0
            
        job_description = job_description.lower()
        score = 0.0
        
        # Check for key skills
        for category, skills in self.skills.items():
            for skill in skills:
                if skill.lower() in job_description:
                    score += 1.0
        
        # Check for leadership terms
        leadership_terms = ['lead', 'head', 'director', 'manage', 'strategy']
        for term in leadership_terms:
            if term in job_description:
                score += 0.5
        
        # Check for marketing terms
        marketing_terms = ['marketing', 'growth', 'acquisition', 'content', 'social media']
        for term in marketing_terms:
            if term in job_description:
                score += 0.5
        
        # Extra points for Web3/Blockchain
        if 'web3' in job_description or 'blockchain' in job_description:
            score += 2.0
            
        return min(score / 10.0, 1.0)  # Normalize to 0-1 range
