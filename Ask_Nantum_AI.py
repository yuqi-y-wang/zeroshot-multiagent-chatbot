## chainlit run app.py -w 
import logging
import os
import uuid
import asyncio
import torch
import pandas as pd
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
import streamlit as st
from MODULES import config, Logger
from AGENTS.Doorman import Doorman
# from fireworks.client import AsyncFireworks

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# Log the import of modules
logger.info("Imported all necessary modules")

# Set default dtype
torch.set_default_dtype(torch.float32)
torch.set_default_tensor_type('torch.FloatTensor')
logger.info("Set default PyTorch dtype and tensor type")

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
logger.info("Set CUDA_VISIBLE_DEVICES to -1")

# Initialize clients and logger
try:
    client_openai = AsyncOpenAI(api_key=config.OPENAI_API_KEY)
    client_anthropic = AsyncAnthropic(api_key=config.ANTHROPIC_API_KEY)
    # client_fireworks = AsyncFireworks(api_key=config.FIREWORKS_API_KEY)

    logger.info("Initialized OpenAI and Anthropic clients")
except Exception as e:
    logger.error(f"Error initializing API clients: {str(e)}")
    raise
if "session_id" not in st.session_state:
        st.session_state["session_id"] = str(uuid.uuid4())
logger_instance = Logger.Logger()
agent = Doorman(logger_instance, client_openai, client_anthropic, None,  None)
logger.info("Initialized Logger and Doorman agent")

import streamlit.components.v1 as components
import base64

def download_button(label, data, file_name, mime):
    b64 = base64.b64encode(data).decode()
    custom_css = f"""
        <style>
            #downloadButton {{
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: 0.25rem 0.75rem;
                border-radius: 0.25rem;
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.25rem;
                font-size: 1rem;
                user-select: none;
                vertical-align: middle;
                text-align: center;
                text-decoration: none;
                cursor: pointer;
            }}
        </style>
    """
    button_html = f'{custom_css}<a id="downloadButton" href="data:{mime};base64,{b64}" download="{file_name}">{label}</a>'
    return components.html(button_html, height=45)

def setup_streamlit():
    st.title("Nantum AI Chatbot")
    st.caption("Ask Nantum AI Chatbot for energy efficiency and compliance")
    # if "session_id" not in st.session_state:
    #     st.session_state["session_id"] = str(uuid.uuid4())
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "files_to_delete" not in st.session_state:
        st.session_state["files_to_delete"] = []
    logger.info("Streamlit setup completed")

def handle_message(message):
    logger.info(f"Handling message: {message[:50]}...")  # Log first 50 chars of message
    answer = agent.serve_user_query(message)
    logger.info("Message handled successfully")
    return answer

async def display_chat():
    # Initialize file_info in session state if it doesn't exist
    if "file_info" not in st.session_state:
        st.session_state.file_info = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Display existing file download buttons
    for file_info in st.session_state.file_info:
        create_download_button(file_info)

    prompt = st.chat_input()
    if prompt:
        logger.info(f"Received user prompt: {prompt[:50]}...")  # Log first 50 chars of prompt
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        with st.spinner("Nantum is working..."):
            answer, file_names = await agent.serve_user_query(prompt)
            logger.info(f"Agent response received. File names: {file_names}")
            if file_names:
                for f in file_names:
                    st.session_state["files_to_delete"].append(f)
                    file_info = process_file(f)
                    if file_info:
                        st.session_state.file_info.append(file_info)
                        create_download_button(file_info)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.chat_message("assistant").write(answer)
            logger.info("Chat display updated with assistant's response")

def process_file(file_path):
    file_extension = file_path[-4:]
    try:
        if file_extension == '.csv':
            data = pd.read_csv(file_path)
            logger.info(f"Successfully read CSV file: {file_path}")
            csv_data = data.to_csv(index=False).encode('utf-8')
            return {"path": file_path, "data": csv_data, "type": "csv"}
        elif file_extension == '.png':
            with open(file_path, "rb") as file:
                image_data = file.read()
            logger.info(f"Successfully read PNG file: {file_path}")
            return {"path": file_path, "data": image_data, "type": "png"}
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {str(e)}")
    return None

# from download_button import download_button

def create_download_button(file_info):
    if file_info["type"] == "csv":
        download_button(
            f'Download {file_info["path"]}',
            file_info["data"],
            file_info["path"],
            'text/csv'
        )
    elif file_info["type"] == "png":
        download_button(
            f"Download {file_info['path']}",
            file_info["data"],
            file_info["path"],
            "image/png"
        )
        st.image(file_info["path"], caption=file_info["path"].split('/')[-1])
    logger.info(f"Created download button for file: {file_info['path']}")

async def main():
    setup_streamlit()
    logger.info("Application started")
    try:
        await display_chat()
    except Exception as e:
        logger.error(f"An error occurred in main execution: {str(e)}", exc_info=True)
    finally:
        # Delete all files created during the session
        for file in st.session_state["files_to_delete"]:
            try:
                os.remove(file)
                logger.info(f"Deleted file: {file}")
            except Exception as e:
                logger.error(f"Error deleting file {file}: {str(e)}")
        st.session_state["files_to_delete"] = []
        st.session_state["file_info"] = []  # Clear file_info as well
    
        
if __name__ == "__main__":
    logger.info("Starting main execution")
    asyncio.run(main())
    logger.info("Main execution completed")

## This is for using chainlit
# import chainlit as cl
# app = App()