import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LinkedIn API Keys
    LINKEDIN_CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID')
    LINKEDIN_CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
    
    # Job Search Parameters
    LOCATIONS = ['Austin, TX', 'Remote']
    KEYWORDS = ['Marketing Director', 'Head of Marketing', 'VP Marketing', 'Growth Marketing', 'Web3 Marketing']
    EXPERIENCE_LEVEL = 'senior'
    
    # Application Settings
    MAX_APPLICATIONS_PER_DAY = 20
    AUTO_APPLY = True
    
    # Resume Path
    RESUME_PATH = 'data/resume.pdf'
