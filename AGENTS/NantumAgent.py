from AGENTS.GeneralAgent import GeneralAgent
from MODULES import config, Logger, paths
from DATA.SYSTEM_PROMPTS import NantumAgent_prompts

class NantumAgent(GeneralAgent):
    def __init__(self, logger, client_openai, client_anthropic, client_fireworks, retriever):
        super().__init__(logger, client_openai, client_anthropic, client_fireworks, retriever)
        self.prompt_template = None
        self.agent_type = "NantumAgent"
        self.system_prompt = NantumAgent_prompts

    async def serve_user_query(self, user_query):
        # Read log content
        log_content = self.logger.get_chat_history(full=False)
        
        # # Create initial system prompt
        msg = self.system_prompt.default_system_prompt(user_query, log_content)

        # Retrieve relevant information from the document
        reference = self.retriever.search(query=msg, k=3)
        full_reference = "".join(page['content'] for page in reference)
        
        # Create final system prompt with references
        msg = self.system_prompt.nantum_agent_system_prompt(
            user_query, log_content, full_reference)
        
        # # Update conversation log with the final system prompt
        ## Get response from API communicator
        response = await self.API_communicator(
           msg, **config.nantum_agent_settings)
        # Update conversation log with the response
        return response
