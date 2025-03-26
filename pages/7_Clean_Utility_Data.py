import streamlit as st
import requests
import datetime
import pandas as pd


portfolio_id = st.text_input('Portfolio Id')
site_id = st.text_input('Site Id')
email = st.text_input('Email')
utility_type = st.selectbox('Utility Type', ['Electric', 'Gas', 'Steam'])
utility_data_type = st.selectbox('Utility Data Type', ['Consumption', 'Demand'])
device_id = st.text_input('Device Id or Sensor Id[optional]')
start_date = st.text_input('Start Date (YYYY-MM-DD) [optional]')
end_date = st.text_input('End Date (YYYY-MM-DD) [optional]')

def run_clean_data(portfolio_id, site_id, email, utility_type, utility_data_type, start_date, end_date):
    print("portfolio_id: ", portfolio_id)
    print("site_id: ", site_id)
    print("email: ", email)
    print("utility_type: ", utility_type)
    print("utility_data_type: ", utility_data_type)
    print("start_date: ", start_date)
    print("end_date: ", end_date)
    if utility_data_type == 'Consumption':
        resource = f'{utility_type.lower()}_consumption'
    elif utility_data_type == 'Demand':
        resource = f'{utility_type.lower()}_demand'
    else:
        st.error('Utility Data Type not supported')
        return
    if start_date:
        start_date = pd.to_datetime(start_date).strftime('%Y-%m-%d')
    if end_date:
        end_date = pd.to_datetime(end_date).strftime('%Y-%m-%d')
    if start_date and end_date:
        if start_date > end_date:
            st.error('Start Date should be less than End Date')
            return
    if start_date and end_date:
        payload = {
            "company": portfolio_id,
            "building": site_id,
            "resource": resource,
            "start_date": start_date,
            "end_date": end_date,
            "email": email
        }
    else:
        payload = {
            "company": portfolio_id,
            "building": site_id,
            "resource": resource,
            "email": email
        }
    if device_id:
        payload['device_id'] = device_id
    # Code to clean the utility data
    url='https://66s0jdipch.execute-api.us-east-1.amazonaws.com/dev/v1/onboarding/cleaned_data'
    response = requests.post(url, json=payload)
    if response.status_code != 202:
        st.error('Failed to clean utility data')
        return
    st.success(f'Successfully initiated utility data cleaning process, {email} will receive an email with the results shortly.')


if st.button('Clean Data'):
    run_clean_data(portfolio_id, site_id, email, utility_type, utility_data_type, start_date, end_date)
