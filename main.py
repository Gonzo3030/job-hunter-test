import argparse
from src.core.job_hunter import JobHunter

def main():
    parser = argparse.ArgumentParser(description='AI Job Hunter')
    parser.add_argument('--search', action='store_true', help='Search for new jobs')
    parser.add_argument('--review', action='store_true', help='Review saved jobs')
    args = parser.parse_args()

    hunter = JobHunter()

    if args.search:
        print('Starting job search...')
        hunter.hunt_jobs()
    elif args.review:
        print('Reviewing saved jobs...')
        # TODO: Implement review functionality
    else:
        print('Please specify an action: --search or --review')

if __name__ == '__main__':
    main()
