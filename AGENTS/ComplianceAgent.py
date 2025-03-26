from AGENTS.GeneralAgent import GeneralAgent
from MODULES import config, Logger, paths
from DATA.SYSTEM_PROMPTS import ComplianceAgent_prompts

class ComplianceAgent(GeneralAgent):
    def __init__(self, logger, client_openai, client_anthropic, client_fireworks, retriever):
        super().__init__(logger, client_openai, client_anthropic, client_fireworks, retriever)
        self.task_api_name = "compliance"
        self.prompt_template = ComplianceAgent_prompts
        self.agent_type = "ComplianceAgent"

    async def serve_user_query(self, user_query):
        log_content = self.logger.get_chat_history(full=False)
        examples = self.find_relevant_examples(user_query)
        msg = self.prompt_template.default_system_prompt(user_query, log_content, examples)
        response = await self.API_communicator(
            msg, **config.compliance_agent_settings)
        code = self.extract_code_from_GPT_response(response)
        if code:
            response = self.code_executor(code)
        return response
