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

    def validate_token_permissions(self):
        """Validate that the token has the necessary permissions.
        
        Returns:
            tuple: (is_valid, error_message)
        """
        # First, check if we can access the user endpoint
        url = f'{self.base_url}/user'
        response = requests.get(url, headers=self.headers)
        
        if response.status_code != 200:
            try:
                error_details = response.json()
                return False, f"Token validation failed: {error_details.get('message', 'Unknown error')}"
            except:
                return False, f"Token validation failed: HTTP {response.status_code}"
        
        user_data = response.json()
        print(f"✅ Token is valid for user: {user_data.get('login', 'Unknown')}")
        
        # Check token scopes (if available in headers)
        scopes = response.headers.get('X-OAuth-Scopes', '')
        if scopes:
            print(f"🔑 Token scopes: {scopes}")
            
            # Check if we have the necessary scopes
            scope_list = [s.strip() for s in scopes.split(',')]
            if 'user' not in scope_list and 'public_repo' not in scope_list and 'repo' not in scope_list:
                return False, f"Token missing required scopes. Has: [{scopes}] but needs: 'user' or 'repo'"
        else:
            print("🔑 Token scopes not available in response (fine-grained token)")
        
        return True, "Token validation successful"

    def test_star_permissions(self, test_repo=None):
        """Test if we can actually star/unstar repositories.
        
        Args:
            test_repo (dict): Optional repository to test with
            
        Returns:
            bool: True if permissions work, False otherwise
        """
        if not test_repo:
            print("⚠️  No test repository provided, skipping permission test")
            return True
        
        owner = test_repo['owner']['login']
        repo_name = test_repo['name']
        
        print(f"🧪 Testing star/unstar permissions on {owner}/{repo_name}...")
        
        # Check if already starred
        check_url = f'{self.base_url}/user/starred/{owner}/{repo_name}'
        print(f"   Debug: Testing URL: {check_url}")
        check_response = requests.get(check_url, headers=self.headers)
        print(f"   Debug: GET response: {check_response.status_code}")
        was_starred = check_response.status_code == 204
        
        if was_starred:
            print(f"   Repository is currently starred")
            # Try to unstar temporarily
            unstar_response = requests.delete(check_url, headers=self.headers)
            if unstar_response.status_code == 204:
                print("   ✅ Unstar test successful")
                # Re-star it
                star_response = requests.put(check_url, headers=self.headers)
                if star_response.status_code == 204:
                    print("   ✅ Re-star test successful")
                    return True
                else:
                    print(f"   ❌ Re-star failed: {star_response.status_code}")
                    return False
            else:
                print(f"   ❌ Unstar test failed: {unstar_response.status_code}")
                try:
                    error_details = unstar_response.json()
                    print(f"      Error: {error_details.get('message', 'Unknown error')}")
                except:
                    pass
                return False
        else:
            print(f"   Repository is currently not starred, skipping test")
            return True

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
            str: "success", "not_found", "permission_denied", or "error"
        """
        url = f'{self.base_url}/user/starred/{owner}/{repo_name}'
        response = requests.delete(url, headers=self.headers)

        if response.status_code == 204:
            print(f'✅ Successfully unstarred: {owner}/{repo_name}')
            return "success"
        elif response.status_code == 404:
            print(f'ℹ️  Repository not found (likely deleted/moved): {owner}/{repo_name}')
            return "not_found"
        elif response.status_code == 403:
            # Enhanced error reporting for permission issues
            error_msg = f'❌ Permission denied for {owner}/{repo_name}'
            try:
                error_details = response.json()
                if 'message' in error_details:
                    error_msg += f' - {error_details["message"]}'
            except:
                pass
            print(error_msg)
            return "permission_denied"
        else:
            # Enhanced error reporting for other issues
            error_msg = f'❌ Failed to unstar {owner}/{repo_name}: {response.status_code}'
            try:
                error_details = response.json()
                if 'message' in error_details:
                    error_msg += f' - {error_details["message"]}'
            except:
                # If response isn't JSON, just show the text
                if response.text.strip():
                    error_msg += f' - {response.text.strip()}'
            
            print(error_msg)
            return "error"

        if response.status_code == 204:
            print(f'✅ Successfully unstarred: {owner}/{repo_name}')
            return "success"
        elif response.status_code == 404:
            print(f'ℹ️  Repository not found (likely deleted/moved): {owner}/{repo_name}')
            return "not_found"
        elif response.status_code == 403:
            # Enhanced error reporting for permission issues
            error_msg = f'❌ Permission denied for {owner}/{repo_name}'
            try:
                error_details = response.json()
                if 'message' in error_details:
                    error_msg += f' - {error_details["message"]}'
            except:
                pass
            print(error_msg)
            return "permission_denied"
        else:
            # Enhanced error reporting for other issues
            error_msg = f'❌ Failed to unstar {owner}/{repo_name}: {response.status_code}'
            try:
                error_details = response.json()
                if 'message' in error_details:
                    error_msg += f' - {error_details["message"]}'
            except:
                # If response isn't JSON, just show the text
                if response.text.strip():
                    error_msg += f' - {response.text.strip()}'
            
            print(error_msg)
            return "error"

    def remove_stars_from_inactive_repos(self, years_threshold=5):
        """Main method to remove stars from inactive repositories.
        
        Args:
            years_threshold (int): Years of inactivity threshold
        """
        # First validate token permissions
        print("🔍 Validating GitHub token permissions...")
        is_valid, error_msg = self.validate_token_permissions()
        if not is_valid:
            print(f"❌ {error_msg}")
            return False
        
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
        failed_count = 0
        not_found_count = 0
        permission_denied_count = 0
        failed_repos = []
        not_found_repos = []
        
        for repo in inactive_repos:
            owner = repo['owner']['login']
            repo_name = repo['name']

            result = self.unstar_repo(owner, repo_name)
            if result == "success":
                unstarred_count += 1
            elif result == "not_found":
                not_found_count += 1
                not_found_repos.append(f"{owner}/{repo_name}")
            elif result == "permission_denied":
                permission_denied_count += 1
                failed_repos.append(f"{owner}/{repo_name}")
            else:
                failed_count += 1
                failed_repos.append(f"{owner}/{repo_name}")

            # Rate limiting
            time.sleep(0.5)

        # Improved reporting
        total_processed = unstarred_count + not_found_count
        print(f"Successfully processed {total_processed} repositories:")
        print(f"  • Unstarred: {unstarred_count}")
        print(f"  • Already deleted/moved: {not_found_count}")
        
        if permission_denied_count > 0:
            print(f"❌ Permission denied for {permission_denied_count} repositories")
            if permission_denied_count <= 5:
                for repo in failed_repos[:permission_denied_count]:
                    print(f"   • {repo}")
            print("\n💡 This indicates insufficient token permissions.")
            print("   Please ensure your GitHub token has 'user' scope.")
            return False
            
        if failed_count > 0:
            print(f"❌ Other failures: {failed_count} repositories")
            if failed_count <= 3:
                remaining_failed = [r for r in failed_repos if r not in failed_repos[:permission_denied_count]]
                for repo in remaining_failed[:3]:
                    print(f"   • {repo}")
                    
        return True


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
