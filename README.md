# aws-s3-wrapper
# AWS S3 Wrapper

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

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/bhagyabinoy/aws-s3-wrapper.git
   cd aws-s3-wrapper
