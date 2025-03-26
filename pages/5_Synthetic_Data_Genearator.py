from datetime import datetime
import streamlit as st
import pandas as pd
import os
import zipfile
import boto3
from io import BytesIO

# Reuse the existing function to upload file to S3
def upload_to_s3(bucket_name, file_name, data):
    s3 = boto3.client('s3')
    s3.upload_fileobj(data, bucket_name, file_name)
    st.success('Calculations job submitted successfully, you will receive an email with the results shortly.')

# Function for the new feature
# def upload_monthly_utility_data():
st.markdown('<div class="app-header"><h1>Synthetic Data Generation</h1></div>', unsafe_allow_html=True)

# User email input
email = st.text_input("Enter your email", "")

# Dropdown for utility type
utility_type = st.selectbox("Utility", ["Gas", "Steam", "Electric"])

# Radio button for utility data type
utility_data_type = st.radio("Utility Type", ["Consumption", "Demand"])

# File uploader for the monthly utility data CSV
utility_data_file = st.file_uploader("Upload Monthly Utility Data CSV", type=['csv'], key="utility_data")

# Text inputs for similar company and building in Nantum
similar_company = st.text_input('Enter Similar Company in Nantum', '')
similar_building = st.text_input('Enter Similar Building ID in Nantum', '')

# Button to process the file
if st.button('Upload Data'):
    if email and utility_data_file and similar_company and similar_building:
        # Create email.csv and add it to the files_to_upload
        email_df = pd.DataFrame([email], columns=['email'])
        email_df["utility_type"] = utility_type
        email_df["utility_data_type"] = utility_data_type
        email_csv = email_df.to_csv(index=False).encode('utf-8')
        files_to_upload = {'email.csv': BytesIO(email_csv), 'monthly_utility_data.csv': utility_data_file}

        # Zip the files
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
            for file_name, file_data in files_to_upload.items():
                if isinstance(file_data, BytesIO):  # For email.csv
                    zip_file.writestr(file_name, file_data.getvalue())
                else:  # For utility_data_file
                    zip_file.writestr(file_name, file_data.read())

        zip_buffer.seek(0)

        # Upload the zip file to S3
        bucket_name = 'cr-synthetic-data-input-data-bucket'
        current_date = datetime.now().strftime('%Y-%m-%d')
        zip_file_name = f'{similar_company}/{similar_building}/{current_date}/utility_data.zip'
        upload_to_s3(bucket_name, zip_file_name, zip_buffer)
    else:
        st.error('Please enter all required fields and upload the monthly utility data file.')

# Call the function to render it in the Streamlit app
# upload_monthly_utility_data()