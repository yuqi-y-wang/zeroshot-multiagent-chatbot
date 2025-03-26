import os
os.environ["API_HOST"]=""
os.environ["CONSUMER_KEY"] = ""
os.environ["CONSUMER_SECRET"]=""

import requests
from an_common.resource import get_resource_doc, get_readings_df, get_building_metadata, \
get_readings_df_interpolation, get_sensor_metadata
import pandas as pd
from an_common.api import get_app_data
## Function to Load data

def get_device_ids(company, building, resource):
  df = get_sensor_metadata(company, building, resource)
  return df[df['identifier3'] == 'total']['_id'].to_list()

def get_savings_for_one_day(company, building, resource, date):
  df = get_sensor_metadata(company, building, resource)
  device_ids = df[df['identifier3'] == 'total']['_id'].to_list()
  body={"company": company,
          "building": building,
          "target_commands": [{"command": "startup", "resource": "commands"}, 
                              {"command": "lunch_rampup", "resource": "commands"}, 
                                {"command": "lunch_rampdown", "resource":   "commands"},
                                  {"command": "final_rampdown", "resource": "commands"}, 
                                  {"command": "shutdown", "resource": "commands"}],
          "startup_indicator": {"resource": "supply_fan_status", "device_ids": []},
          "temperature_indicator": {"resource": "interior_space_temperature", "device_ids": []},
          "utility_indicator": {"resource": resource, "device_ids": device_ids},
          "callback_url": ""}
  onboarding = requests.post(url="",
                          json=body, headers={"x-api-key":""})

  inference = requests.get(url="", 
                          params={"company": company, 
                                  "building": building, 
                                  "date": date,
                                  "device_ids": device_ids}, 
                                  headers={"x-api-key":""})
  return eval(inference.text)