import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LinkedIn API Keys
    LINKEDIN_CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID')
    LINKEDIN_CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
    
    # Job Search Parameters
    LOCATIONS = ['Remote', 'Austin, TX']
    KEYWORDS = [
        'Head of Marketing',
        'Head of Growth',
        'Head of Partnerships',
        'Head of Business Development',
        'Director of Marketing',
        'Marketing Director',
        'Growth Director',
        'VP Marketing',
        'VP Growth',
        'Web3 Marketing',
        'Blockchain Marketing'
    ]

    # Target Industries/Companies
    TARGET_INDUSTRIES = [
        'web3',
        'blockchain',
        'crypto',
        'defi',
        'technology',
        'software',
        'saas',
        'startup',
        'fintech',
        'artificial intelligence',
        'ai',
        'machine learning'
    ]
    
    # Must exclude terms (filter out jobs with these terms)
    EXCLUDE_TERMS = [
        'junior',
        'associate',
        'coordinator',
        'entry level'
    ]
    
    # Application Settings
    MAX_APPLICATIONS_PER_DAY = 20
    AUTO_APPLY = True
    
    # Resume Path
    RESUME_PATH = 'data/resume.pdf'
