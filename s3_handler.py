import boto3
import io
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class S3Handler:
    def __init__(self):
        self.AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
        self.AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
        self.AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')

    def connect_to_s3(self):
        print("AWS S3 connection called")
        """Connect to S3 and return the bucket resource."""
        try:
            s3 = boto3.resource(
                's3',
                aws_access_key_id=self.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
                region_name=self.AWS_S3_REGION_NAME
            )
            bucket = s3.Bucket(self.AWS_STORAGE_BUCKET_NAME)
            return bucket
        except ClientError as e:
            print(f"Error connecting to S3: {str(e)}")
            return None

    def get_object_key(self, key):
        return f"app/{key}"

    def generate_presigned_url(self, key, expiration=86400):
        """Generate a presigned URL for an S3 object."""
        signed_url = None
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=self.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
                region_name=self.AWS_S3_REGION_NAME
            )
            signed_url = s3_client.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': self.AWS_STORAGE_BUCKET_NAME,
                    'Key': self.get_object_key(key)
                },
                ExpiresIn=expiration
            )
        except ClientError as e:
            print(f"Error generating presigned URL: {str(e)}")
        return signed_url

    def upload_image(self, image_file, key):
        """Upload an image to S3."""
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=self.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
                region_name=self.AWS_S3_REGION_NAME
            )
            s3_client.upload_fileobj(image_file, self.AWS_STORAGE_BUCKET_NAME, self.get_object_key(key))
            return True
        except ClientError as e:
            print(f"Error uploading image: {str(e)}")
            return False

    def download_image(self, key):
        """Download an image from S3."""
        buffer = io.BytesIO()
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=self.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
                region_name=self.AWS_S3_REGION_NAME
            )
            s3_client.download_fileobj(self.AWS_STORAGE_BUCKET_NAME, self.get_object_key(key), buffer)
            buffer.seek(0)
            return buffer
        except ClientError as e:
            print(f"Error downloading image: {str(e)}")
            return None

    def delete_object(self, key):
        """Delete an object from S3."""
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=self.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
                region_name=self.AWS_S3_REGION_NAME
            )
            s3_client.delete_object(Bucket=self.AWS_STORAGE_BUCKET_NAME, Key=self.get_object_key(key))
            return True
        except ClientError as e:
            print(f"Error deleting object: {str(e)}")
            return False

    def list_objects(self, prefix=''):
        """List objects in the S3 bucket."""
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=self.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
                region_name=self.AWS_S3_REGION_NAME
            )
            response = s3_client.list_objects_v2(Bucket=self.AWS_STORAGE_BUCKET_NAME, Prefix=self.get_object_key(prefix))
            return [obj['Key'] for obj in response.get('Contents', [])]
        except ClientError as e:
            print(f"Error listing objects: {str(e)}")
            return []

    def object_exists(self, key):
        """Check if an object exists in the S3 bucket."""
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=self.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
                region_name=self.AWS_S3_REGION_NAME
            )
            s3_client.head_object(Bucket=self.AWS_STORAGE_BUCKET_NAME, Key=self.get_object_key(key))
            return True
        except ClientError:
            return False

    def copy_object(self, source_key, dest_key):
        """Copy an object within S3."""
        copy_source = {
            'Bucket': self.AWS_STORAGE_BUCKET_NAME,
            'Key': self.get_object_key(source_key)
        }
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=self.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
                region_name=self.AWS_S3_REGION_NAME
            )
            s3_client.copy(copy_source, self.AWS_STORAGE_BUCKET_NAME, self.get_object_key(dest_key))
            return True
        except ClientError as e:
            print(f"Error copying object: {str(e)}")
            return False

    def move_object(self, source_key, dest_key):
        """Move (rename) an object in S3."""
        if self.copy_object(source_key, dest_key):
            self.delete_object(source_key)
            return True
        return False


if __name__ == "__main__":
    s3_handler = S3Handler()

    # List objects in the S3 bucket
    print("Listing objects in S3 bucket:")
    objects = s3_handler.list_objects()
    print(objects)

    # Check if an object exists
    key_to_check = 'test_image.jpg'
    exists = s3_handler.object_exists(key_to_check)
    print(f"Does {key_to_check} exist? {'Yes' if exists else 'No'}")

    # Copy an object
    if s3_handler.copy_object(key_to_check, 'copy_of_test_image.jpg'):
        print("Object copied successfully.")

    # Move an object
    if s3_handler.move_object('copy_of_test_image.jpg', 'moved_image.jpg'):
        print("Object moved successfully.")
