from interpreter import interpreter
import nbformat
from MODULES import config

import an_common
from an_common.api import get_app_data
from an_common.resource import get_building_metadata, get_readings_df_interpolation, \
    get_sensor_metadata, get_resource_doc, get_readings_df, get_building_metadata, \
get_readings_df_interpolation, get_sensor_metadata

import os
os.environ["API_HOST"]=""
os.environ["CONSUMER_KEY"] = ""
os.environ["CONSUMER_SECRET"]=""
os.environ["OPENAI_API_KEY"]=""

def cal_token_cost(num_token, model, input=True):
    if input:
        return num_token * config.price_dict['input'][model]
    else:
        return num_token * config.price_dict['output'][model]

def cal_cost_openai(response, model):
    input_cost = cal_token_cost(response.usage.prompt_tokens, 
                                model, 
                                input=True)
    print('input_cost: ', input_cost)
    output_cost = cal_token_cost(response.usage.completion_tokens, 
                                model, 
                                input=False)
    print('output_cost: ', output_cost)
    return input_cost + output_cost

def cal_cost_anthropic(response):
    input_cost = cal_token_cost(response.usage.input_tokens, 
                                "claude-3-5-sonnet-20240620", 
                                input=True)
    print('input_cost: ', input_cost)
    output_cost = cal_token_cost(response.usage.output_tokens, 
                                "claude-3-5-sonnet-20240620", 
                                input=False)
    print('output_cost: ', output_cost)
    return input_cost + output_cost

def cal_cost_fireworks(response):
    input_cost = cal_token_cost(response.usage.prompt_tokens, 
                                response.model, 
                                input=True)
    print('input_cost: ', input_cost)
    output_cost = cal_token_cost(response.usage.completion_tokens, 
                                response.model, 
                                input=False)
    print('output_cost: ', output_cost)
    return input_cost + output_cost

# def extract_code_from_GPT_response(content):
#     """Extract code from GPT response."""
#     try:
#         return content.split("```python")[1].split("```")[0]
#     except:
#         return None
    
# def code_executor(code):
#     """Interpreter for code."""
#     return interpreter.computer.run("python", code)[0]['content']

def summarize_ipynb(ipynb_path):
    """Summarizes an ipynb file by extracting code and markdown cells."""
    with open(ipynb_path, 'r', encoding='utf-8') as file:
        nb = nbformat.read(file, as_version=4)
    
    summary = []
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            # Extracting code cells
            summary.append('### Code\n')
            summary.append(cell['source'])
        elif cell['cell_type'] == 'markdown':
            # Extracting markdown cells
            summary.append('### Markdown\n')
            summary.append(cell['source'])
    
    # Joining all parts into a single string
    return '\n'.join(summary)

