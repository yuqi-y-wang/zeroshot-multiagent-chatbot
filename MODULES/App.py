import openai
from openai import AsyncOpenAI

from MODULES import config, Logger
from AGENTS.Doorman import Doorman
import anthropic
from anthropic import AsyncAnthropic

import streamlit as st

class App:
    def __init__(self):
        self.client_openai = AsyncOpenAI(api_key=config.OPENAI_API_KEY)
        self.client_anthropic = AsyncAnthropic(api_key=config.ANTHROPIC_API_KEY)
        self.logger = Logger.Logger()
        self.agent = Doorman(self.logger, self.client_openai, self.client_anthropic)

    async def run(self, message):
        answer = await self.agent.serve_user_query(message)
        return answer

## the following is for chainlit
# import chainlit as cl
# class App:
#     def __init__(self):
#         self.client_openai = AsyncOpenAI(api_key=config.OPENAI_API_KEY)
#         self.client_anthropic = AsyncAnthropic(api_key=config.ANTHROPIC_API_KEY)
#         cl.instrument_openai()
#         self.logger = Logger.Logger()
#         self.agent = Doorman(self.logger, self.client_openai, self.client_anthropic)

#     async def run(self, message):
#         answer = await self.agent.serve_user_query(message)
#         return answer
