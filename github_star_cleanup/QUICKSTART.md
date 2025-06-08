# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Setup

Run the setup script to create a virtual environment and install dependencies:

```bash
./setup.sh
```

Or use the Makefile:

```bash
make setup
```

### Step 2: Configure GitHub Token

1. Get a GitHub Personal Access Token:

   - Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
   - Click "Generate new token" (classic)
   - Select the `user` scope (to read/write starred repositories)
   - Copy the generated token

2. Add your token to the `.env` file:
   ```bash
   # Edit the .env file
   nano .env
   # Change: GITHUB_TOKEN=your_github_token_here
   # To: GITHUB_TOKEN=ghp_your_actual_token_here
   ```

### Step 3: Run the Script

```bash
# Option 1: Use the run script
./run.sh

# Option 2: Use the Makefile
make run

# Option 3: Manual activation
source venv/bin/activate
python github_star_cleanup_clean.py
```

## 📁 Project Files

- `github_star_cleanup_clean.py` - Main script (improved version)
- `github_star_cleanup.py` - Original script
- `example_usage.py` - Example of programmatic usage
- `setup.sh` - Setup script
- `run.sh` - Quick run script
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

To change the inactivity threshold, edit the `years_threshold` parameter in the script or modify the `main()` function.

## 🔒 Safety Features

- **Confirmation prompt** - Always asks before unstarring
- **Rate limiting** - Respects GitHub API limits
- **Error handling** - Graceful error recovery
- **Virtual environment** - Isolated dependencies
