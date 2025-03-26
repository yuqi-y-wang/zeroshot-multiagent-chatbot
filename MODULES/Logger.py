import datetime
import boto3
from botocore.exceptions import ClientError
import streamlit as st
from io import BytesIO
import logging
logger = logging.getLogger(__name__)

class Logger:
    def __init__(self):
        current_date = datetime.datetime.now().strftime("%Y/%m/%d")
        self.session_id = st.session_state["session_id"]
        self.log_folder = f"{current_date}/conversation_{self.session_id}"
        self.bucket_name = "cr-ask-nantum"
        self.s3_client = boto3.client('s3')
        # self.ensure_unique_filename()
        self.log_filename_visible = f"{self.log_folder}/visible.txt"
        self.log_filename_full = f"{self.log_folder}/full.txt"
    
    def ensure_unique_filename(self):
        pass
        # counter = 1
        # original_folder = self.log_folder
        # while self.object_exists(f"{self.log_folder}/"):
        #     self.log_folder = f"{original_folder}-{counter}"
        #     counter += 1

    def object_exists(self, key):
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=key)
            return True
        except ClientError:
            return False

    def log_message(self, role, message, full=True):
        log_path = self.log_filename_full if full else self.log_filename_visible
        content = f"{role}: {message['content'] if isinstance(message, dict) else message}\n"
        
        try:
            # Read existing content
            logger.info(f"Reading from {log_path}")
            existing_content = self.read_file(log_path)
            # Append new content
            updated_content = existing_content + content
            # Write updated content back to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=log_path,
                Body=updated_content,
                ACL='private'
            )
            logger.info(f"Writing to {log_path}")
        except ClientError as e:
            st.error(f"Error writing to S3: {str(e)}")

    def read_file(self, file_path):
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_path)
            return response['Body'].read().decode('utf-8')
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                # File doesn't exist yet, return empty string
                return ''
            else:
                st.error(f"Error reading from S3: {str(e)}")
                return ''

    def get_chat_history(self, full=False):
        log_path = self.log_filename_full if full else self.log_filename_visible
        return self.read_file(log_path)