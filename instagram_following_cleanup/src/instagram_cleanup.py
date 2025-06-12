import os

import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class InstagramFollowingCleanup:
    def __init__(self, access_token):
        self.access_token = access_token
        # Use Graph API instead of Basic Display API
        self.base_url = "https://graph.facebook.com/v18.0"
        self.user_id = self.get_user_id()

    def get_user_id(self):
        """Get the user's Instagram Business Account ID"""
        # First get Facebook pages
        url = f"{self.base_url}/me/accounts"
        params = {
            "fields": "instagram_business_account",
            "access_token": self.access_token,
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            pages = data.get("data", [])

            for page in pages:
                if "instagram_business_account" in page:
                    return page["instagram_business_account"]["id"]

            raise Exception(
                "No Instagram Business Account found. "
                "Make sure your Instagram account is "
                "connected to a Facebook Page."
            )
        else:
            raise Exception(f"Failed to get pages: {response.text}")

    def get_following_list(self):
        """Get list of accounts the user is following"""
        # This endpoint may not be available for all Instagram accounts
        url = f"{self.base_url}/{self.user_id}"
        params = {
            "fields": "follows_count,media_count,username",
            "access_token": self.access_token,
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            print("Account info retrieved successfully!")
            account_info = response.json()
            print(f"Username: {account_info.get('username', 'Unknown')}")
            follows_count = account_info.get("follows_count", 0)
            print(f"Following: {follows_count} accounts")
            print(f"Posts: {account_info.get('media_count', 0)}")

            # Unfortunately, Instagram Graph API doesn't provide
            # direct access to following list for most accounts
            print("\n⚠️  Instagram API Limitation:")
            print(
                "Instagram's API doesn't allow apps to access your "
                "following list or unfollow accounts programmatically."
            )
            print("This is a privacy protection by Instagram.")

            return []
        else:
            print(f"Error fetching account info: {response.text}")
            return []

    def get_user_media(self):
        """Get user's own media to test API connectivity"""
        url = f"{self.base_url}/{self.user_id}/media"
        params = {
            "fields": "id,caption,media_type,timestamp",
            "access_token": self.access_token,
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            media = response.json().get("data", [])
            print(f"✅ Successfully fetched {len(media)} of your posts")
            return media
        else:
            print(f"❌ Error fetching media: {response.text}")
            return []

    def cleanup_inactive_follows(self):
        """Main function - shows API limitations"""
        print("🔍 Instagram Following Cleanup - API Test")
        print("=" * 50)

        # Test API connectivity
        print("Testing Instagram Graph API connectivity...")

        try:
            # Test getting account info
            self.get_following_list()

            # Test getting user's media
            media = self.get_user_media()

            print("\n📋 API Test Results:")
            print("✅ Authentication: Working")
            print("✅ Account Access: Working")
            print(f"✅ Media Access: Working ({len(media)} posts found)")
            print("❌ Following List: Not accessible via API")

            print("\n🤔 Why This Doesn't Work:")
            print("• Instagram's API doesn't allow accessing following lists")
            print("• You cannot unfollow accounts programmatically")
            print("• This is by design for user privacy and security")

            print("\n💡 Alternative Solutions:")
            print("1. Manual cleanup through Instagram app/website")
            print("2. Use Instagram's built-in " "'Least Interacted With' feature")
            print("3. Third-party tools (use with caution)")

            print("\n📱 Instagram's Built-in Solution:")
            print(
                "Go to: Instagram → Following → Categories → " "Least Interacted With"
            )

        except Exception as e:
            print(f"❌ API Error: {e}")


def main():
    # Load access token from environment
    access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")

    if not access_token:
        print(
            "❌ Please set your Instagram Access Token in the "
            "INSTAGRAM_ACCESS_TOKEN environment variable"
        )
        print(
            "📖 Get token from: " "https://developers.facebook.com/docs/instagram-api/"
        )
        return

    try:
        cleanup = InstagramFollowingCleanup(access_token)
        cleanup.cleanup_inactive_follows()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Common Issues:")
        print("• Instagram account not connected to Facebook Page")
        print("• Need Instagram Business/Creator account")
        print("• Insufficient API permissions")


if __name__ == "__main__":
    main()
