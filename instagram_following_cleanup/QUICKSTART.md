# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Setup

Run the setup script to create a virtual environment and install dependencies:

```bash
make setup
```

Or use the script directly:

```bash
./scripts/setup.sh
```

### Step 2: Configure Instagram Access Token

1. Get an Instagram Access Token:
   - Go to [Instagram Developers](https://developers.facebook.com/docs/instagram-basic-display-api)
   - Create a new app and set up Instagram Basic Display API
   - Generate an access token with required permissions
   - Copy the generated token

2. Add your token to the `.env` file:

   ```bash
   cp .env.example .env
   # Edit the .env file
   nano .env
   # Change: INSTAGRAM_ACCESS_TOKEN=your_instagram_access_token_here
   # To: INSTAGRAM_ACCESS_TOKEN=your_actual_token_here
   ```

### Step 3: Run the Script

```bash
# Option 1: Use the Makefile
make run

# Option 2: Use the run script
./scripts/run.sh

# Option 3: Manual activation
source venv/bin/activate
python src/instagram_cleanup.py
```

## 📁 Project Files

- `src/instagram_cleanup.py` - Main cleanup script
- `instagram_cleanup.py` - Alternative main script location
- `scripts/setup.sh` - Setup script
- `scripts/run.sh` - Quick run script
- `scripts/utils.sh` - Utility functions
- `Makefile` - Make commands for easy management
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variable template
- `README.md` - Full documentation

## 🛠️ Available Commands

```bash
# Setup project
make setup

# Run the cleanup
make run

# Show help
make help

# Clean up (remove venv)
make clean

# Code linting
make lint
```

## ⚙️ Customization

To change the inactivity threshold, edit the `days=730` parameter in the `cleanup_inactive_follows()` method (730 days = 2 years).

## 🔧 Troubleshooting

### Token Issues

If you see errors related to authentication:

1. **Verify token validity**: Check that your Instagram access token is active
2. **Check permissions**: Ensure the token has necessary scopes for following/unfollowing
3. **API limits**: Instagram has strict rate limits - the script includes delays

### Quick Test

The script will validate your setup and show any issues before starting the cleanup.

## 🔒 Safety Features

- **Confirmation prompt** - Always asks before unfollowing
- **Rate limiting** - Respects Instagram API limits
- **Error handling** - Graceful error recovery
- **Virtual environment** - Isolated dependencies

## 📋 What the Script Does

1. **Fetches following list** - Gets all accounts you follow
2. **Checks activity** - Looks at last post date for each account
3. **Identifies inactive** - Finds accounts with no posts in 2+ years
4. **Asks confirmation** - Shows list and asks permission to unfollow
5. **Unfollows safely** - Removes follows with proper rate limiting

The script is designed to be safe and conservative - it will always ask before making changes to your Instagram account.
