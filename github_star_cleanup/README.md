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
   - Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
   - Click "Generate new token" → "Generate new token (classic)"
   - **Required scopes**:
     - ✅ **`user`** - Access to user profile information and starred repositories
     - ✅ **`public_repo`** - Required to star/unstar public repositories
     - ✅ **`repo`** - (Optional) Only needed if you want to unstar private repositories
   - Copy the generated token

2. Configure the token:
   - Create a `.env` file with your token (recommended - see Environment Variables section)
   - Or replace `'your_github_token_here'` in the script with your actual token

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

## Troubleshooting

### Permission Errors (403/404)

If you get permission errors or "Not Found" errors when trying to unstar repositories:

1. **Check your token scopes**: The token must have `public_repo` scope
   - Run the script to see current scopes: `🔑 Token scopes: gist, public_repo, user`
   - If missing `public_repo`, create a new token with the correct permissions

2. **Fine-grained vs Classic tokens**:
   - **Classic tokens** (recommended): Select `user` + `public_repo` scopes
   - **Fine-grained tokens**: Grant "Starring: Write" permission under Account permissions

### Common Issues

- **"Resource not accessible by personal access token"**: Token missing `public_repo` scope
- **Repository appears starred but unstar fails**: Usually a permissions issue
- **Rate limiting**: The script includes built-in delays, but heavy usage may hit limits

## API Rate Limits

The script includes built-in rate limiting to stay within GitHub's API limits:

- 0.1 second delay when fetching starred repositories
- 0.5 second delay when unstarring repositories

## License

This project is open source and available under the MIT License.
