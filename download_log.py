import boto3
import os

def download_s3_folder(bucket_name, s3_folder, local_dir=None):
    """
    Download the contents of an S3 folder to a local directory
    """
    s3 = boto3.client('s3')
    if local_dir is None:
        local_dir = os.path.join(os.getcwd(), s3_folder.replace('/', '_'))
    
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    paginator = s3.get_paginator('list_objects_v2')
    for result in paginator.paginate(Bucket=bucket_name, Prefix=s3_folder):
        if 'Contents' in result:
            for file in result['Contents']:
                file_key = file['Key']
                if not file_key.endswith('/'):  # Skip folders
                    local_file_path = os.path.join(local_dir, os.path.relpath(file_key, s3_folder))
                    if not os.path.exists(os.path.dirname(local_file_path)):
                        os.makedirs(os.path.dirname(local_file_path))
                    s3.download_file(bucket_name, file_key, local_file_path)
                    print(f"Downloaded {file_key} to {local_file_path}")

if __name__ == "__main__":
    bucket_name = "cr-ask-nantum"
    s3_folder = "2024/08/22/"
    
    download_s3_folder(bucket_name, s3_folder)
    print("Download completed.")