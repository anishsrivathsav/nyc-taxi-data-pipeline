import os
import boto3
import logging
from dotenv import load_dotenv

# ===============================
# Logging Configuration
# ===============================
logging.basicConfig(
    filename='logs/s3_upload.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Also log to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

# ===============================
# S3Uploader Class
# ===============================
class S3Uploader:
    """
    Handles uploading files from a local folder to an AWS S3 bucket.
    Credentials are securely loaded from environment variables.
    """

    def __init__(self,dot_env_path :str,bucket_name:str, s3_prefix:str = ""):
        self.dot_env_path = dot_env_path
        load_dotenv(dotenv_path= dot_env_path)  # Load environment variables from .env
        self.bucket_name = bucket_name
        self.s3_prefix = s3_prefix.rstrip("/") + "/" if s3_prefix else ""

        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_DEFAULT_REGION")
        )

    def upload_folder(self, local_folder: str):
        """
        Recursively uploads all files from local_folder to the S3 bucket, maintaining the folder hierarchy.

        Args:
            local_folder (str): The base local folder to start uploading from (e.g., 'data/')
        """
        logging.info(f"🚀 Starting upload from '{local_folder}' to 's3://{self.bucket_name}/{self.s3_prefix}'")

        for root, dirs, files in os.walk(local_folder):
            for file in files:
                local_path = os.path.join(root, file)

                # Compute relative path from the root folder
                relative_path = os.path.relpath(local_path, local_folder)
                s3_key = os.path.join(self.s3_prefix, relative_path).replace("\\", "/")

                try:
                    self.s3.upload_file(local_path, self.bucket_name, s3_key)
                    logging.info(f"Uploaded: {local_path} → s3://{self.bucket_name}/{s3_key}")
                except Exception as e:
                    logging.error(f" Failed to upload {local_path}: {e}")


# ===============================
# Main Execution
# ===============================
if __name__ == "__main__":
    dot_envpath = os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..",'aws_credentials.env')))
    load_dotenv(dotenv_path= dot_envpath)
    BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
    rootpath = os.path.join(os.getcwd(),'data')
    S3_PREFIX = "raw"
    uploader = S3Uploader(bucket_name=BUCKET_NAME, dot_env_path =dot_envpath,  s3_prefix=S3_PREFIX)
    uploader.upload_folder(rootpath)