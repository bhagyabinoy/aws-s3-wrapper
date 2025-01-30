import os
from google.oauth2 import id_token
from google.auth.transport import requests

# Replace this with your actual Google OAuth2 client secret
GOOGLE_CLIENT_SECRET = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")

# Mock database for storing users
USER_DATABASE = {}

def verify_google_token(token):
    """Verify the Google OAuth2 token and return user data."""
    if not token:
        raise ValueError("Token is required")

    try:
        return id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_SECRET)
    except ValueError:
        raise ValueError("Invalid token")
    except Exception as e:
        raise RuntimeError(f"Token verification error: {str(e)}")

def get_or_create_user(user_data):
    """Retrieve an existing user or create a new one."""
    email = user_data.get('email')
    first_name = user_data.get('given_name', '')
    last_name = user_data.get('family_name', '')

    if not email:
        raise ValueError("Email is required")

    # Check if the user exists in the mock database
    user = USER_DATABASE.get(email)
    if not user:
        user = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "username": email,  # Use email as username
            "password": None,  # No password for social auth users
        }
        USER_DATABASE[email] = user  # Save user to mock database

    return user

def google_signup(token):
    """
    Sign up a user using Google authentication.
    Returns a dictionary with user details or an error message.
    """
    try:
        # Verify token and extract user details
        user_data = verify_google_token(token)
        user = get_or_create_user(user_data)

        return {"message": "User signed up successfully", "user_data": user}, 201

    except ValueError as e:
        return {"error": str(e)}, 400
    except RuntimeError as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    test_token = "your_google_oauth_token_here"
    response, status_code = google_signup(test_token)
    print(f"Response ({status_code}):", response)
