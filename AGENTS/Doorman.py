from DATA.SYSTEM_PROMPTS import Doorman_prompts
from MODULES import config, Logger, paths
from AGENTS.GeneralAgent import GeneralAgent
from AGENTS.RawDataRetrieverAgent import RawDataRetrieverAgent
from AGENTS.MVAgent import MVAgent
from AGENTS.NantumAgent import NantumAgent
from AGENTS.ComplianceAgent import ComplianceAgent
import asyncio
from ragatouille import RAGPretrainedModel
import re
import ast

class Doorman(GeneralAgent):
    def __init__(self, logger, client_openai, client_anthropic, client_fireworks, retriever):
        super().__init__(logger, client_openai, client_anthropic, client_fireworks, retriever)
        self.agent_type = "Doorman"
        self.agents = dict()
        self.prompt_template = Doorman_prompts
        self.user_query = None
        self.nantum_retriever = RAGPretrainedModel.from_index(paths.nantum_doc_index_path)
        self.coding_retriever = RAGPretrainedModel.from_index(paths.coding_index_path)
        self.agents['GeneralAgent'] = GeneralAgent(logger, client_openai, client_anthropic, client_fireworks, None)
        self.agents["RawDataRetrieverAgent"] = RawDataRetrieverAgent(logger, client_openai, client_anthropic, client_fireworks, self.coding_retriever)
        self.agents["MVAgent"] = MVAgent(logger, client_openai, client_anthropic, client_fireworks, self.coding_retriever)
        self.agents["NantumAgent"] = NantumAgent(logger, client_openai, client_anthropic, client_fireworks, self.nantum_retriever)
        self.agents['ComplianceAgent'] = ComplianceAgent(logger, client_openai, client_anthropic, client_fireworks, self.coding_retriever)

    async def task_assigner(self, user_query):
            """
            Processes the user query to assign the task 
            to a proper agent, and logs the conversation.
            
            Args:
                user_query (str): The query from the user.
            
            Returns:
                dict: A dictionary containing the assigned agent 
                name and the sub-question for that agent.
            """
            self.user_query = user_query
            ## save user query
            self.logger.log_message('user', user_query, full=False)
            self.logger.log_message('user', user_query, full=True)
            ## create prompt with chat history
            log_content = self.logger.get_chat_history(full=False)
            msg = self.prompt_template.default_system_prompt(user_query, log_content)
            response = await self.API_communicator(msg, **config.task_assigner_settings)
            return response

    async def write_final_answer(self, user_query, assigned_agents_names, answers):
        """
        Processes the agent's answer and assigns the task to a proper agent if the answer is not good. Logs the conversation.
        
        Args:
            assigned_agent_s_answer (str): The answer from the assigned agent.
        
        Returns:
            str: The final answer to the user.
        """
        log_content = self.logger.get_chat_history(full=False)
        msg = self.prompt_template.merge_question_prompt(
            user_query, assigned_agents_names, answers, log_content)
        response = await self.API_communicator(msg, **config.final_answer_settings)     
        return response 
    
    def create_agent(self, assigned_agent):
        # agent_class = globals()[assigned_agent]
        # if assigned_agent == 'NantumAgent':
        #     return agent_class(self.logger, self.client, self.ragatouille_pack)
        # else:
        #     return agent_class(self.logger, self.client)
        return self.agents[assigned_agent]

    def create_agents_from_names(self, assigned_agents):
        return [self.create_agent(assigned_agent) for assigned_agent in assigned_agents]
    
    async def serve_user_query(self, user_query):
        GeneralAgent.reset_total_cost()
        response = await self.task_assigner(user_query)
        print('DOORMAN RESPONSE: ', response)
        try:
            try:
                assigned_agents_and_subquestions = eval(response)
            except:
                assigned_agents_and_subquestions = self.extract_code_from_GPT_response(response)
                assigned_agents_and_subquestions = eval(assigned_agents_and_subquestions)            
            assigned_agents = self.create_agents_from_names(list(assigned_agents_and_subquestions.keys())) 
            questions = list(assigned_agents_and_subquestions.values())
            questions = ["".join(question) if isinstance(question, list) else [question] for question in questions]
            assigned_agents_answers = await self.get_assigned_agent_answer(assigned_agents, questions)
            final_answer = await self.write_final_answer(
                user_query, assigned_agents_and_subquestions, assigned_agents_answers)  
        except:
            final_answer = await self.write_final_answer(
                user_query, None, response) 
        try:
            response_content = final_answer
            text_match = re.search(r'"text"\s*:\s*"((?:[^"\\]|\\.)*)"', response_content, re.DOTALL)
            if text_match:
                final_answer = text_match.group(1)
                final_answer = final_answer.replace('\\n', '\n')  # Replace '\n' with actual newline
            else:
                print("Couldn't find 'text' field in the response.")
            # Extract file_names if present
            elements = []
            file_names_match = re.search(r'"file_names"\s*:\s*(\[[^\]]*\])', response_content)
            if file_names_match:
                file_names_str = file_names_match.group(1)
                elements = ast.literal_eval(file_names_str)
            else:
                print("\nCouldn't find 'file_names' field in the response.")
        except:
            elements = None
        # The following is for chainlit
        # elements = None
        # if file_names:
        #     elements = [
        #         cl.File(
        #         name=file_name,
        #         path=file_name,
        #         display="inline",
        #     ) for file_name in file_names
        # ]
        
        self.logger.log_message('Assistant', final_answer, full=False)
        final_cost = GeneralAgent.get_total_cost()/1_000_000
        print(f"Total cost for this query: ${final_cost}")
        self.logger.log_message('Assistant', f"Total cost for this query: ${final_cost}", full=True)
        return final_answer, elements
    
    async def get_assigned_agent_answer(self, assigned_agents, subquestions):
        tasks = [agent.serve_user_query(subquestion) for agent, subquestion in zip(assigned_agents, subquestions)]
        results = await asyncio.gather(*tasks)
        # Destroy the assigned agents after getting results
        return results
