DATA_PATH = 'DATA/'
CONVERSATION_HISTORY_PATH = DATA_PATH + 'CONVERSATION_HISTORY/'
CODE_REFERENCE_PATH = DATA_PATH + 'CODE_REFERENCES/'
CODE_REFERENCE_ENVIRONMENT_HELPER_PATH = CODE_REFERENCE_PATH + 'ENVIRONMENT/'
CODE_REFERENCE_EXAMPLE_PATH = CODE_REFERENCE_PATH + 'EXAMPLES/'
CODE_REFERENCE_DOCUMENT_PATH = CODE_REFERENCE_PATH + 'DOCUMENTS/'

SYSTEM_PROMPT_PATH = DATA_PATH + 'SYSTEM_PROMPTS/'

code_executor_environment_helper_paths = {
    'an_common': CODE_REFERENCE_ENVIRONMENT_HELPER_PATH +'an_common_env.py',
    'm_and_v': CODE_REFERENCE_ENVIRONMENT_HELPER_PATH + 'm_and_v_env.py',
    'compliance': CODE_REFERENCE_ENVIRONMENT_HELPER_PATH + 'compliance_env.py',
    # 'specify_parameters': CODE_REFERENCE_ENVIRONMENT_HELPER_PATH + 'specify_parameters.txt',
}

code_example_paths = {
    'an_common': CODE_REFERENCE_EXAMPLE_PATH + 'an_common.ipynb',
    'm_and_v': CODE_REFERENCE_EXAMPLE_PATH + 'm_and_v.ipynb',
    'compliance': CODE_REFERENCE_EXAMPLE_PATH + 'compliance.ipynb',
    # 'specify_parameters': CODE_REFERENCE_EXAMPLE_PATH + 'specify_parameters.ipynb',
}

# code_document_paths = {
#     'an_common': [CODE_REFERENCE_DOCUMENT_PATH + '',]
# }

nantum_doc_pdf_path = DATA_PATH + 'NANTUM_DOC/PD Research.pdf'
nantum_doc_index_path = '.ragatouille/colbert/indexes/nantum_doc'
coding_index_path = '.ragatouille/colbert/indexes/coding_examples'