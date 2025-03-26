from datetime import datetime
import streamlit as st
import pandas as pd
import os
import zipfile
import boto3
from io import BytesIO

# Function to upload file to S3
def upload_to_s3(bucket_name, file_name, data):
    s3 = boto3.client('s3')
    s3.upload_fileobj(data, bucket_name, file_name)
    st.success('Calculations job submitted successfully, you will receive an email with the results shortly.')

# Streamlit app with design improvements for dark theme
st.markdown('<div class="app-header"><h1>Potential savings calculator</h1></div>', unsafe_allow_html=True)

# User email input with some spacing
email = st.text_input("Enter your prescriptive data email", "")

# File uploaders for each CSV file in a 2-column layout with added spacing
files_to_upload = {}
file_names = ['load_df.csv', 'startup_data.csv', 'location.csv', 'shutdown_data.csv', 'ramps_data.csv', 'fan_data.csv', 'adm_settings.csv']
cols = st.columns(2)  # Create two columns
col_index = 0  # To alternate between columns
company = cols[0].text_input('Enter Company Name', '')
building = cols[1].text_input('Enter Building Name', '')
for file_name in file_names:
    with cols[col_index]:
        # st.markdown(f'<div class="upload-box"><p class="medium-font">{file_name}</p>', unsafe_allow_html=True)
        file = st.file_uploader(file_name, type=['csv'], key=file_name)
        if file is not None:
            files_to_upload[file_name] = file
        col_index = 1 - col_index  # Alternate column

# Button to process the files with some spacing above
if st.button('Upload Files'):
    if email and len(files_to_upload) == 7:  # Check if email is provided and all files are uploaded
        # Create email.csv and add it to the files_to_upload
        email_df = pd.DataFrame([email], columns=['email'])
        email_csv = email_df.to_csv(index=False).encode('utf-8')
        files_to_upload['email.csv'] = BytesIO(email_csv)

        # Zip the files
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
            for file_name, file_data in files_to_upload.items():
                zip_file.writestr(file_name, file_data.getvalue())
        zip_buffer.seek(0)

        # Upload the zip file to S3
        bucket_name = 'cr-potential-savings-input-data-bucket'
        current_date = datetime.now().strftime('%Y-%m-%d')
        print(company, building, current_date)
        zip_file_name = f'{company}/{building}/{current_date}/data.zip'
        upload_to_s3(bucket_name, zip_file_name, zip_buffer)
    else:
        st.error('Please enter your email and upload all files.')
