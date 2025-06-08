#!/usr/bin/env python3
"""
Example usage of the GitHub Star Cleanup tool
"""

import os
from github_star_cleanup_clean import GitHubStarManager

def example_usage():
    """Example of how to use the GitHubStarManager programmatically"""
    
    # Get token from environment
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("Please set GITHUB_TOKEN environment variable")
        return
    
    # Create manager instance
    manager = GitHubStarManager(token)
    
    # Example 1: Just get starred repos without unstarring
    print("Fetching starred repositories...")
    repos = manager.get_starred_repos()
    print(f"You have {len(repos)} starred repositories")
    
    # Example 2: Check which repos are inactive (without unstarring)
    inactive_count = 0
    for repo in repos:
        if not manager.is_recently_active(repo, years_threshold=5):
            inactive_count += 1
            print(f"Inactive: {repo['full_name']} (last updated: {repo.get('updated_at', 'N/A')})")
    
    print(f"\nFound {inactive_count} inactive repositories (5+ years)")
    
    # Example 3: Custom threshold - check for 2 years instead of 5
    print("\nChecking with 2-year threshold:")
    inactive_2_years = 0
    for repo in repos:
        if not manager.is_recently_active(repo, years_threshold=2):
            inactive_2_years += 1
    
    print(f"Repositories inactive for 2+ years: {inactive_2_years}")
    
    # Note: To actually unstar, use:
    # manager.remove_stars_from_inactive_repos(years_threshold=5)

if __name__ == "__main__":
    example_usage()
