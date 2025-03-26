import requests
import json
import pandas as pd
import os
os.environ["API_HOST"]=""
os.environ["CONSUMER_KEY"] = ""
os.environ["CONSUMER_SECRET"]=""
from an_common.day_type import cal_day_type

url=""
api_key = ""
ecms = ["startup", "shutdown", "lunch_rampdown", "lunch_rampup", "final_rampdown", "shutdown"]

def check_valid_dates(start_date, end_date, company, building):
    day_type_out = cal_day_type(company, building, None, start_date, end_date, use_beta=None)
    return day_type_out


def get_compliance_data(company, building, date, ecm_command_type='all'):
    df = pd.DataFrame(columns=['date', 'ecm_command_type', 'complied'])
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    if ecm_command_type== 'all':
        ecm_command_types = ecms
    elif isinstance(ecm_command_type, list):
        ecm_command_types = ecm_command_type
    else:
        ecm_command_types = [ecm_command_type]
    for ecm in ecm_command_types:
        params = {
            "company": company,
            "building": building,
            "date": date,
            "ecm_command_type":ecm,
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code != 200:
            new_row = pd.DataFrame({'date': [date], 'ecm_command_type': [None], 'complied': [None]})
            df = pd.concat([df, new_row], ignore_index=True)
        elif response.json()['status'] == 'complied':
            new_row = pd.DataFrame({'date': [date], 'ecm_command_type': [ecm], 'complied': [True]})
            df = pd.concat([df, new_row], ignore_index=True)
        else:
            new_row = pd.DataFrame({'date': [date], 'ecm_command_type': [ecm], 'complied': [False]})
            df = pd.concat([df, new_row], ignore_index=True)
    return df
  
    # status would be either:
    # complied, not_complied or unknown
    # message: success or description or the problem