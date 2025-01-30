# AWS S3 Wrapper -> s3_handler.py

`aws-s3-wrapper` is a Python library for simplified interactions with Amazon S3. This wrapper provides a straightforward API for common S3 operations such as uploading, downloading, deleting, copying, and listing objects in S3 buckets. It uses `boto3` for AWS service integration and loads configuration from a `.env` file using `python-dotenv`.

## Features

- Upload images and files to S3
- Download files from S3
- Delete objects from S3
- Generate presigned URLs for secure access
- List objects in a bucket
- Check if an object exists in a bucket
- Copy and move objects within the same bucket

## Requirements

- Python 3.6 or higher
- `boto3`
- `python-dotenv`

# Chrome Version Detector -> chrome-version.py  
This Python script determines the version of Google Chrome installed on a system. It is designed to work across multiple operating systems, including Windows, Linux, and macOS, and employs various methods to retrieve the Chrome version based on the platform.

## Features
- Detects the platform (Windows, Linux, or macOS) using subprocess.
- Retrieves the Chrome version through:
   - Windows Registry queries.
   - Installation folder scanning on Windows.
   - Executing the Chrome binary with the --version flag on Linux and macOS.
   - Provides fallback mechanisms for robustness.

## Requirements
   - Python 3.x: Ensure Python is installed on your system.
   - Google Chrome: The script requires Google Chrome to be installed to retrieve its version.
   - Permissions: On Windows, ensure the script has sufficient permissions to query the registry.

## How It Works
1. Platform Detection
The script uses the uname command for Linux and macOS detection. If unavailable, it defaults to Windows (win32).

2. Chrome Version Retrieval
   Windows:
   Queries the Windows registry for the Chrome version.
   Scans the common installation directories (C:\Program Files and C:\Program Files (x86)).
   Linux/macOS:
   Executes the Chrome binary located at its default installation path (e.g., /usr/bin/google-chrome on Linux or /Applications/Google Chrome.app/... on macOS) with the --version flag.
   3. Output
   The detected Chrome version is printed. If Chrome is not installed or the version cannot be determined, an appropriate message is displayed.

# Google Signup -> google_auth_signup.py  

### Overview
This script handles Google OAuth2 authentication for user signup. It verifies a Google token, retrieves user details, and stores them in a mock database.  

### Usage  
1. Set your Google OAuth2 client secret as an environment variable:  
   ```bash
   export SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET="your_google_client_secret"
   ```
2. Run the script with a valid Google token:  
   ```python
   from google_auth_signup import google_signup

   token = "your_google_oauth_token_here"
   response, status_code = google_signup(token)
   print(response, status_code)
   ```
   
### Requirements
- Python 3.x  
- `google-auth` library (`pip install google-auth google-auth-oauthlib`)  

