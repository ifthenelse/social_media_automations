import requests
from datetime import datetime, timedelta
import time
import os


def load_env_file():
    """Load environment variables from .env file if it exists"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()


class GitHubStarManager:
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.base_url = 'https://api.github.com'
    
    def get_starred_repos(self):
        """Get all starred repositories for the authenticated user"""
        starred_repos = []
        page = 1
        
        while True:
            url = f'{self.base_url}/user/starred'
            params = {'page': page, 'per_page': 100}
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            repos = response.json()
            if not repos:
                break
                
            starred_repos.extend(repos)
            page += 1
            
            # Rate limiting
            time.sleep(0.1)
        
        return starred_repos
    
    def is_recently_active(self, repo, years_threshold=5):
        """Check if repository was active within the specified years"""
        last_activity = repo.get('updated_at') or repo.get('pushed_at')
        if not last_activity:
            return False
        
        last_activity_date = datetime.strptime(last_activity, '%Y-%m-%dT%H:%M:%SZ')
        threshold_date = datetime.now() - timedelta(days=years_threshold * 365)
        
        return last_activity_date > threshold_date
    
    def unstar_repo(self, owner, repo_name):
        """Remove star from a repository"""
        url = f'{self.base_url}/user/starred/{owner}/{repo_name}'
        response = requests.delete(url, headers=self.headers)
        
        if response.status_code == 204:
            print(f'Successfully unstarred: {owner}/{repo_name}')
            return True
        else:
            print(f'Failed to unstar {owner}/{repo_name}: {response.status_code}')
            return False
    
    def remove_stars_from_inactive_repos(self, years_threshold=5):
        """Main method to remove stars from repositories inactive for specified years"""
        print("Fetching starred repositories...")
        starred_repos = self.get_starred_repos()
        print(f"Found {len(starred_repos)} starred repositories")
        
        inactive_repos = []
        
        for repo in starred_repos:
            if not self.is_recently_active(repo, years_threshold):
                inactive_repos.append(repo)
        
        print(f"Found {len(inactive_repos)} repositories inactive for more than {years_threshold} years")
        
        if not inactive_repos:
            print("No repositories to unstar.")
            return
        
        # Confirm before proceeding
        confirm = input(f"Do you want to unstar {len(inactive_repos)} repositories? (y/N): ")
        if confirm.lower() != 'y':
            print("Operation cancelled.")
            return
        
        unstarred_count = 0
        for repo in inactive_repos:
            owner = repo['owner']['login']
            repo_name = repo['name']
            
            if self.unstar_repo(owner, repo_name):
                unstarred_count += 1
            
            # Rate limiting
            time.sleep(0.5)
        
        print(f"Successfully unstarred {unstarred_count} repositories")

def main():
    # Replace with your GitHub personal access token
    GITHUB_TOKEN = 'your_github_token_here'
    
    if GITHUB_TOKEN == 'your_github_token_here':
        print("Please replace 'your_github_token_here' with your actual GitHub token")
        return
    
    try:
        manager = GitHubStarManager(GITHUB_TOKEN)
        manager.remove_stars_from_inactive_repos(years_threshold=5)
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()