#!/usr/bin/env python3
"""
GitHub Star Cleanup Script

A tool to automatically unstar GitHub repositories that have been inactive
for a specified period of time.
"""

import os
import time
from datetime import datetime, timedelta

import requests


def load_env_file():
    """Load environment variables from .env file if it exists."""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()


class GitHubStarManager:
    """Manages GitHub starred repositories and provides cleanup functionality."""

    def __init__(self, token):
        """Initialize the GitHub API client.
        
        Args:
            token (str): GitHub personal access token
        """
        self.token = token
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.base_url = 'https://api.github.com'

    def get_starred_repos(self):
        """Get all starred repositories for the authenticated user.
        
        Returns:
            list: List of starred repository data from GitHub API
        """
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
        """Check if repository was active within the specified years.
        
        Args:
            repo (dict): Repository data from GitHub API
            years_threshold (int): Number of years to consider as threshold
            
        Returns:
            bool: True if repository is recently active, False otherwise
        """
        last_activity = repo.get('updated_at') or repo.get('pushed_at')
        if not last_activity:
            return False

        last_activity_date = datetime.strptime(
            last_activity, '%Y-%m-%dT%H:%M:%SZ'
        )
        threshold_date = datetime.now() - timedelta(
            days=years_threshold * 365
        )

        return last_activity_date > threshold_date

    def unstar_repo(self, owner, repo_name):
        """Remove star from a repository.
        
        Args:
            owner (str): Repository owner/organization
            repo_name (str): Repository name
            
        Returns:
            bool: True if successful, False otherwise
        """
        url = f'{self.base_url}/user/starred/{owner}/{repo_name}'
        response = requests.delete(url, headers=self.headers)

        if response.status_code == 204:
            print(f'Successfully unstarred: {owner}/{repo_name}')
            return True
        else:
            print(f'Failed to unstar {owner}/{repo_name}: '
                  f'{response.status_code}')
            return False

    def remove_stars_from_inactive_repos(self, years_threshold=5):
        """Main method to remove stars from inactive repositories.
        
        Args:
            years_threshold (int): Years of inactivity threshold
        """
        print("Fetching starred repositories...")
        starred_repos = self.get_starred_repos()
        print(f"Found {len(starred_repos)} starred repositories")

        inactive_repos = []

        for repo in starred_repos:
            if not self.is_recently_active(repo, years_threshold):
                inactive_repos.append(repo)

        print(f"Found {len(inactive_repos)} repositories inactive for "
              f"more than {years_threshold} years")

        if not inactive_repos:
            print("No repositories to unstar.")
            return

        # Confirm before proceeding
        prompt = (f"Do you want to unstar {len(inactive_repos)} "
                 f"repositories? (y/N): ")
        confirm = input(prompt)
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
    """Main function to run the GitHub star cleanup."""
    # Load environment variables from .env file
    load_env_file()
    
    # Try to get token from environment variable first, then fallback
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', 'your_github_token_here')

    if GITHUB_TOKEN == 'your_github_token_here':
        print("Please set your GitHub token either:")
        print("1. In a .env file: GITHUB_TOKEN=your_token_here")
        print("2. As an environment variable: export GITHUB_TOKEN=your_token")
        print("3. Replace 'your_github_token_here' in the script")
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
