import pandas as pd
import json
import streamlit as st
import requests
from an_common.resource import get_sensor_metadata


def get_building_sensors(company, namespace):
    building_sensors = get_sensor_metadata(company, namespace)
    print(building_sensors["resource"].unique())
    return building_sensors


def onboard_startup(company, building_namespace, startup_indicator, temperature_source, sla_time, floor_zone):
    end_date = pd.Timestamp.now().strftime("%Y-%m-%d")
    start_date = (pd.Timestamp.now() - pd.Timedelta(days=240)).strftime("%Y-%m-%d")
    # Define the payload
    payload = json.dumps({
        "company": company,
        "building": building_namespace,
        "startup_indicator": startup_indicator,
        "temperature_indicator": temperature_source,
        "sla_time": sla_time,
        "floor": floor_zone,
        "callback_url": "https://ayyjyee936.execute-api.us-east-1.amazonaws.com/Prod/callback",
        "gran": 5,
        "start_date": start_date,
        "end_date": end_date
    })
    # print(payload)
    # return {'status_code': 200}
    # Define the headers
    api_key="O9NqhE51gxqJQSh4VI1iayd0H0sVFfv27OGgPq56"
    headers = {
        "Content-Type": "application/json",
        'x-api-key': api_key
    }

    # Define the URL

    url = 'https://yz90151m31.execute-api.us-east-1.amazonaws.com/Prod/startupmodeltraining/'
    # Call the API
    response = requests.post(url, data=payload, headers=headers)

    return response

# Define the fields
st.markdown("<h1 style='text-align: center; color: white;'>Onprem Model Generation</h1>", unsafe_allow_html=True)
company = st.text_input('Company')
building_namespace = st.text_input('Building Namespace')
startup_indicator = st.text_input('Startup Indicator')
temperature_source = st.text_input('Temperature Source')
sla_time = st.text_input('SLA Time')
floor_zone = st.text_input('Floor/Zone')
user_email = st.text_input('Email for notification')

# Convert floor_zone to a list
floor_zone = [item.strip() for item in floor_zone.split(',')]

def check_sensor_is_active(sensor):
    if sensor['status'] == 'active':
        return True
    return False

def check_sensor_last_times_is_greater_than_yesterday(sensor):
    if pd.Timestamp(sensor['last_time'], tz="UTC") > pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=1):
        return True
    return False

# Trigger the backend service
floor_job_arns = {}
if st.button('Onboard Startup'):
    with st.spinner('Processing...'):
        building_sensors = get_building_sensors(company=company, namespace=building_namespace)
        startup_sensors = building_sensors[building_sensors['resource'] == startup_indicator]
        temperature_source_sensors = building_sensors[building_sensors['resource'] == temperature_source]
        if len(startup_sensors) == 0:
            st.error('Startup Indicator not found in the building.')
        elif len(temperature_source_sensors) == 0:
            st.error('Temperature Source not found in the building.')
        else:
            active_fan_sensors = startup_sensors[startup_sensors.apply(check_sensor_is_active, axis=1)]
            active_temperature_sensors = temperature_source_sensors[temperature_source_sensors.apply(check_sensor_is_active, axis=1)]
            if len(active_fan_sensors) == 0:
                st.error('No active Startup Indicator data found in the building.')
            active_fan_data_sensors = active_fan_sensors[active_fan_sensors.apply(check_sensor_last_times_is_greater_than_yesterday, axis=1)]
            if len(active_fan_data_sensors) == 0:
                st.error('No startup indicator sensor with actively sending data found for the building.')
            elif len(active_temperature_sensors) == 0:
                st.error('No active Temperature Source found in the building.')
            active_temperature_data_sensors = active_temperature_sensors[
                active_temperature_sensors.apply(check_sensor_last_times_is_greater_than_yesterday, axis=1)]
            if len(active_temperature_data_sensors) == 0:
                st.error('No temperature indicator sensor with actively sending data found for the building.')
            if not floor_zone or floor_zone[0] == "":
                response = onboard_startup(company, building_namespace, 
                        startup_indicator={"resource": startup_indicator,
                        "device_id": active_fan_data_sensors["_id"].to_list()},
                        temperature_source={"resource": temperature_source,
                        "device_id": active_temperature_data_sensors["_id"].to_list()},
                                            sla_time=sla_time, floor_zone=None)
                if response.status_code != 200:
                    st.error('Failed to onboard startup.')
                else:
                    st.success('Successfully Initiated Startup Model Generation Process.')
            else:
                for floor in floor_zone:
                    # Call the API for each floor
                    floor_startup_sensors = startup_sensors[startup_sensors['floor'] == floor]
                    floor_temperature_source_sensors = temperature_source_sensors[temperature_source_sensors['floor'] == floor]
                    if len(floor_startup_sensors) == 0:
                        st.error('Startup Indicator not found in the floor: {}'.format(floor))
                    elif len(floor_temperature_source_sensors) == 0:
                        st.error('Temperature Source not found in the floor: {}'.format(floor))
                    else:
                        active_floor_startup_sensors = floor_startup_sensors[floor_startup_sensors.apply(check_sensor_is_active, axis=1)]
                        active_floor_temperature_sensors = floor_temperature_source_sensors[floor_temperature_source_sensors.apply(check_sensor_is_active, axis=1)]
                        if len(active_floor_startup_sensors) == 0:
                            st.error('No active Startup Indicator sensor found in the floor: {}'.format(floor))
                        active_floor_startup_data_sensors = active_floor_startup_sensors[active_floor_startup_sensors.apply(check_sensor_last_times_is_greater_than_yesterday, axis=1)]
                        if len(active_floor_startup_data_sensors) == 0:
                            st.error('No startup indicator sensor with actively sending data found for the floor: {}'.format(floor))
                        if len(active_floor_temperature_sensors) == 0:
                            st.error('No active Temperature Source sensor found in the floor: {}'.format(floor))
                        active_floor_temperature_data_sensors = active_floor_temperature_sensors[active_floor_temperature_sensors.apply(check_sensor_last_times_is_greater_than_yesterday, axis=1)]
                        if len(active_floor_temperature_data_sensors) == 0:
                            st.error('No temperature indicator sensor with actively sending data found for the floor: {}'.format(floor))

                        response = onboard_startup(company, building_namespace, 
                                startup_indicator={"resource": startup_indicator , "device_id": active_floor_startup_data_sensors["_id"].to_list()},
                                temperature_source={"resource": temperature_source,
                                "device_id": active_floor_temperature_data_sensors["_id"].to_list()},
                                                    sla_time=sla_time, floor_zone=floor)
                        print(response.status_code)
                        print(response.content)
                        if response.status_code != 200:
                            st.error('Failed to onboard startup for floor: {}'.format(floor))
                        else:
                            floor_job_arns[floor] = response.content.decode('utf-8')
                            st.success(f'Successfully Initiated Startup Model Generation Process for floor {floor}.')

    print("Floor job arns: ", floor_job_arns)
    requests.post(url="https://yz90151m31.execute-api.us-east-1.amazonaws.com/Prod/check-status",
              json={"job_arns": floor_job_arns, "company": company,
                    "building": building_namespace, "email": user_email}, headers={'X-Amz-Invocation-Type': 'Event'})
    print(response.content)

