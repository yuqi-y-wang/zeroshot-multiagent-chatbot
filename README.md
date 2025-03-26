# README #

# Ask Nantum Chatbot

* This is the repository for the Ask Nantum Chatbot, a chatbot that can answer questions about the Nantum AI.
* version 1.0

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Contributing](#contributing)

=============================================================================================================
## Installation

	pip install -r requirements.txt
=============================================================================================================
## Usage

	streamlit run Ask_Nantum_AI.py
=============================================================================================================
## File Structure

    project-root/
    ├── AGENTS/                           # Directory for agents managing application logic.
    │   ├── __init__.py                   
    │   ├── GeneralAgent.py               # Defines a general-purpose agent, cost calculation, LLM API calls, code execution, etc.  
    │   ├── Doorman.py                    # Process user queries by routing them to the appropriate agent and merging the results.
    │   ├── NantumAgent.py                # (RAG) Answer questions about Nantum AI with RAG and Nantum documentation.
    │   ├── ComplianceAgent.py            # (RAG, coding agent) Answer questions about compliance of Nantum recommendations.
    │   ├── MVAgent.py                    # (RAG, coding agent) Answer M&V questions.
    │   └── RawDataRetrieverAgent.py      # (RAG, coding agent) Retrieve an_common resource data, and calculate GHG emissions and peak demand.
    │
    ├── DATA/                             # Storing coding reference, environment variables, examples, and system prompts.
    │   ├── CODE_REFERENCES/              # Reference materials and code examples for LLMs.
    │   │   ├── DOCUMENTS/                
    │   │   │   ├── company_building_resource_filtered.jsonl  # JSONL file with filtered company, building, and corresponding resource data.
    │   │   │   └── function_specs.txt    # function specifications.
    │   │   ├── ENVIRONMENT/              # Environment-specific scripts and configurations. Inserted in the beginning of the LLM generated code.
    │   │   │   ├── an_common_env.py      
    │   │   │   ├── compliance_env.py    
    │   │   │   └── m_and_v_env.py        
    │   │   └── EXAMPLES/                 # Example files.
    │   │       ├── an_common.ipynb       
    │   │       ├── compliance.ipynb
    │   │       ├── m_and_v.ipynb
    │   │       ├── coding.csv            # CSV with coding examples and snippets. RAG will retrieve relevant examples first.
    │   │       └── query_understanding.jsonl  # JSONL with query parsing examples.
    │   ├── SYSTEM_PROMPTS/
    │   │   ├── ComplianceAgent_prompts.py
    │   │   ├── GeneralAgent_prompts.py
    │   │   ├── MVAgent_prompts.py
    │   │   ├── NantumAgent_prompts.py
    │   │   ├── RawDataRetrieverAgent_prompts.py
    │   │   └── Doorman_prompts.py
    │   ├── NANTUM_DOC/
    │   │   └── PD Research.pdf
    │
    ├── MODULES/                          # Core modules that provide various functionalities and variables across the application.
    │   ├── __init__.py                   # Makes MODULES a Python package, allowing module imports.
    │   ├── App.py                        # Previously written for an initialization of application of the chatbot, doesnt work with streamlit for now.
    │   ├── config.py                     # LLM API keys, LLM settings, LLM prices, number of RAG instances, Agents' LLM choices, etc.
    │   ├── Logger.py                     # Provides logging utilities to standardize logging across the application.
    │   ├── paths.py                      # Central definition of file and directory paths used in the application.
    │   └── utils.py                      # Utility functions that provide common functionality used by various modules: calculating costs, and formatting ipynbs.
    │
    ├── SCRIPTS_MAINTENANCE/              # Scripts used for maintaining and updating the application's operational aspects.
    │   ├── update_index_coding.py        # Script to update the index of coding examples for better retrieval.
    │   └── update_index_nantum_doc.py    # Updates the index for Nantum documentation to enhance search capabilities.
    │
    ├── .ragatouille/                     # Configuration and indexing files for the Colbert model, used internally. Updating by scripts in SCRIPTS_MAINTENANCE.
    │   └── colbert/                      
    │       └── indexes/                  
    │           ├── coding_examples/      # Index files for coding examples (questions only), used in machine learning models.
    │           └── nantum_doc/           # Documentation indexes for Nantum, aiding in quick retrieval and reference.
    │
    ├── .streamlit/                       
    │   └── config.toml                   
    │
    ├── an_common/                        # an_common api, current version v3.0.1
    │
    ├── Ask_Nantum_AI.py                  # The main executable script that launches the Nantum AI chatbot interface.
    ├── requirements.txt                  # Lists all Python libraries required to run the application, used with pip install.
    └── README.md                         # The main documentation file for the project, providing an overview and setup instructions.

=============================================================================================================
## Contributing

  * Modifying RAG references

    - Update `DATA/CODE_REFERENCES/EXAMPLES/coding.csv` and run `python SCRIPTS_MAINTENANCE/update_index_coding.py` to update coding examples RAG references.
    - Update `DATA/NANTUM_DOC/PD Research.pdf` and run `python SCRIPTS_MAINTENANCE/update_index_nantum_doc.py` to update the Nantum documentation RAG references.

* Modifying prompts

    - Modify `DATA/SYSTEM_PROMPTS/` to update prompts.

* Adding new agents

    - Modify `AGENTS/` to add new agents.
    - Modify `MODULES/config.py` to add new agents' LLM choices.
    - Modify `AGENTS/Doorman.py` to add new agents' initializations.
    - Modify `DATA/SYSTEM_PROMPTS/Doorman_prompts.py` to add new agents' descriptions in the task assigner's prompt.
    - Modify `DATA/SYSTEM_PROMPTS/` to add new agents' system prompts.
    - Modify `DATA/CODE_REFERENCES/DOCUMENTS/function_specs.txt` to add new agents' function specifications.
    - Modify `DATA/CODE_REFERENCES/EXAMPLES/coding.csv` to add new agents' coding examples and update the index.
    - Modify `DATA/CODE_REFERENCES/ENVIRONMENT/` to add new agents' environment variables.
    - Modify `DATA/CODE_REFERENCES/EXAMPLES/query_understanding.jsonl` to add new agents' query understanding examples.