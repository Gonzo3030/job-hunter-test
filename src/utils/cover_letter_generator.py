import os
from datetime import datetime
from pathlib import Path

class CoverLetterGenerator:
    def __init__(self):
        # Create cover_letters directory if it doesn't exist
        self.cover_letters_dir = Path('cover_letters')
        self.cover_letters_dir.mkdir(exist_ok=True)

    def generate(self, job_title: str, company_name: str, job_description: str) -> str:
        """Generate a customized cover letter"""
        # Generate the cover letter content
        cover_letter = self._generate_content(job_title, company_name, job_description)
        
        # Create filename using company and date
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{company_name.replace(' ', '_')}_{timestamp}.txt"
        filepath = self.cover_letters_dir / filename
        
        # Save the cover letter
        with open(filepath, 'w') as f:
            f.write(cover_letter)
        
        print(f'Cover letter saved to: {filepath}')
        return cover_letter

    def _generate_content(self, job_title: str, company_name: str, job_description: str) -> str:
        """Generate the actual cover letter content"""
        # Basic template with your background
        cover_letter = f"""Dear Hiring Manager at {company_name},

I am writing to express my strong interest in the {job_title} position at {company_name}. With my extensive experience in marketing leadership roles, including significant achievements in Web3 and blockchain spaces, I am confident in my ability to contribute meaningfully to your team.

Most recently, as Head of Web3 Marketing at Immunefi, I led marketing initiatives that resulted in over $150M in available bug bounties and achieved 10x growth. I built and managed a team of 6 marketers while establishing comprehensive business development and partnership programs.

"""

        # Add customized middle paragraph based on job description
        if job_description:
            key_points = self._extract_key_points(job_description)
            cover_letter += f"Your need for {key_points} aligns perfectly with my experience. "

        # Closing
        cover_letter += f"""

I would welcome the opportunity to discuss how my background and skills would benefit {company_name} and contribute to your continued success.

Best regards,
Ivan Benavides"""

        return cover_letter

    def _extract_key_points(self, job_description: str) -> str:
        """Extract key points from job description to customize letter"""
        key_points = []
        
        # Check for key areas in description
        if 'web3' in job_description.lower() or 'blockchain' in job_description.lower():
            key_points.append('Web3 expertise')
        if 'team' in job_description.lower() or 'leadership' in job_description.lower():
            key_points.append('team leadership')
        if 'growth' in job_description.lower():
            key_points.append('growth marketing')
        if 'strategy' in job_description.lower():
            key_points.append('strategic marketing')
        
        if not key_points:
            return 'marketing leadership and strategic growth'
            
        return ', '.join(key_points)
