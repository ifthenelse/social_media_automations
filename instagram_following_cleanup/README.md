# Instagram Following Cleanup

⚠️ **Important Notice**: Due to Instagram API limitations, this script cannot actually access your following list or unfollow accounts programmatically. This is by design for user privacy and security.

## What This Script Does

- ✅ Tests Instagram API connectivity
- ✅ Shows your account information
- ✅ Demonstrates API capabilities and limitations
- ❌ Cannot access following list (Instagram API restriction)
- ❌ Cannot unfollow accounts (Instagram API restriction)

## Instagram API Limitations

Instagram's API has strict limitations:

1. **No Following List Access**: The API doesn't allow apps to see who you follow
2. **No Unfollow Capability**: You cannot unfollow accounts programmatically
3. **Privacy Protection**: These restrictions protect user privacy
4. **Business Accounts Only**: Most features require Instagram Business accounts

## Alternative Solutions

### 1. Instagram's Built-in Features
Instagram provides built-in tools for managing follows:
- Go to **Following** → **Categories** → **Least Interacted With**
- This shows accounts you rarely interact with
- You can manually unfollow from there

### 2. Manual Review
- Regularly review your following list
- Unfollow inactive accounts manually
- Use Instagram's suggestions

### 3. Third-Party Tools
⚠️ **Use with extreme caution**: Third-party tools may violate Instagram's Terms of Service

## Setup (For API Testing)

### Prerequisites
- Instagram Business or Creator account
- Facebook Page connected to Instagram
- Meta Developer account

### Installation
```bash
make setup
cp .env.example .env
# Edit .env with your token
make run
```

## Getting an Instagram Access Token

1. **Create Meta App**: https://developers.facebook.com/
2. **Add Instagram Graph API** to your app
3. **Connect Instagram Business Account**
4. **Generate access token** with required permissions

## What You'll See When Running

The script will:
1. Test API connectivity
2. Show your account information
3. Explain why following list access isn't available
4. Suggest alternative approaches

## Educational Value

This project demonstrates:
- Instagram Graph API usage
- API authentication and error handling
- Understanding API limitations
- Working with Meta's developer platform

## Available Commands

- `make setup` - Set up virtual environment and install dependencies
- `make install` - Install/update dependencies
- `make run` - Run the Instagram API test script
- `make lint` - Run code linting
- `make clean` - Clean up virtual environment

## Legal and Ethical Notes

- Always respect Instagram's Terms of Service
- Don't use automated tools that violate platform rules
- Understand that API restrictions exist for good reasons
- Consider manual approaches for account management

## Contributing

If Instagram's API changes to allow following list access in the future, contributions to update this script would be welcome.

## License

This project is provided for educational purposes only. Use responsibly and in accordance with Instagram's Terms of Service.
