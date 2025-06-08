# GitHub Star Cleanup

A Python script to automatically unstar GitHub repositories that have been inactive for a specified period.

## Features

- Fetches all your starred repositories
- Identifies repositories inactive for more than a specified number of years (default: 5 years)
- Safely removes stars from inactive repositories with user confirmation
- Includes rate limiting to respect GitHub API limits

## Setup

### Prerequisites

- Python 3.8 or higher
- A GitHub Personal Access Token with appropriate permissions

### Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Create a GitHub Personal Access Token:
   - Go to GitHub Settings > Developer settings > Personal access tokens
   - Generate a new token with `user` scope (for reading/writing starred repositories)
2. Update the script:
   - Replace `'your_github_token_here'` in the `main()` function with your actual token
   - Or set it as an environment variable (see Environment Variables section)

### Environment Variables (Recommended)

Instead of hardcoding your token, you can use an environment variable:

1. Create a `.env` file in the project directory:

   ```
   GITHUB_TOKEN=your_actual_token_here
   ```

2. The script will automatically load it (if you use the enhanced version)

## Usage

Run the script:

```bash
python github_star_cleanup.py
```

The script will:

1. Fetch all your starred repositories
2. Identify inactive ones (older than 5 years by default)
3. Ask for confirmation before unstarring
4. Remove stars from confirmed repositories

### Customizing the threshold

You can modify the `years_threshold` parameter in the `main()` function to change how old a repository needs to be before it's considered for unstarring.

## Safety Features

- **Confirmation prompt**: The script asks for confirmation before unstarring repositories
- **Rate limiting**: Includes delays between API calls to respect GitHub's rate limits
- **Error handling**: Gracefully handles API errors and network issues

## API Rate Limits

The script includes built-in rate limiting to stay within GitHub's API limits:

- 0.1 second delay when fetching starred repositories
- 0.5 second delay when unstarring repositories

## License

This project is open source and available under the MIT License.
