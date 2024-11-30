# AI Job Hunter

## Setup
1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure your `.env` file with your API credentials

## Usage

To search for jobs:
```bash
python main.py --search
```

To review saved jobs:
```bash
python main.py --review
```

## Configuration
Edit the `src/config.py` file to customize:
- Job search keywords
- Locations
- Experience level
- Maximum applications per day
