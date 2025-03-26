from DATA.SYSTEM_PROMPTS import GeneralAgent_prompts
from MODULES import config, Logger, paths, utils
from interpreter import interpreter
import pandas as pd
import json

class GeneralAgent:
    total_cost = 0

    def __init__(self, logger, client_openai, client_anthropic, client_fireworks, retriever):
        self.logger = logger if logger else Logger()
        self.client_openai = client_openai if client_openai else None
        self.client_anthropic = client_anthropic if client_anthropic else None
        self.client_fireworks = client_fireworks if client_fireworks else None
        self.query = ""
        self.reference_lists = []
        self.conversation_log = []
        self.current_answer = None
        self.agent_type = "GeneralAgent"
        self.prompt_template = GeneralAgent_prompts
        self.retriever = retriever
    
    @classmethod
    def add_cost(cls, cost):
        cls.total_cost += cost

    @classmethod
    def reset_total_cost(cls):
        cls.total_cost = 0

    @classmethod
    def get_total_cost(cls):
        return cls.total_cost
    
    async def API_communicator(self, msg, **settings):
        try:
            ## The following is for logging the user's message
            self.conversation_log = self.make_messages_from_prompt(
                msg, messages=self.conversation_log)
            # self.logger.log_message('User', self.conversation_log[-1])
            messages = self.conversation_log[-1]
            ## The following is for communicating with the API
            if isinstance(messages, dict):
                messages = [messages]
            elif isinstance(messages, list):
                pass
            else:
                raise ValueError("Invalid type for messages")

            if 'gpt' in settings['model']:
                print('using gpt')
                response = await self.client_openai.chat.completions.create(
                    messages=messages,
                    **settings
                )
                cost =  utils.cal_cost_openai(response, settings['model'])
                self.current_answer = response.choices[0].message.content
            elif 'claude' in settings['model']:
                print('using claude')
                response = await self.client_anthropic.messages.create(
                    messages=messages,
                    **settings
                )
                cost = utils.cal_cost_anthropic(response)
                self.current_answer = response.content[0].text
            elif 'llama' in settings['model']:
                try:
                    print('using llama')
                    response = self.client_fireworks.chat.completions.create(
                        messages=messages,
                    **settings
                )
                    cost = utils.cal_cost_fireworks(response)
                    self.current_answer = response.choices[0].message.content
                except Exception as e:
                    print(e)
            else:
                raise ValueError("Invalid model")
            
            GeneralAgent.add_cost(cost)
            print(self.agent_type, "   ", cost)
            ## The following is for logging the assistant's response
            self.logger.log_message('assistant', self.current_answer)
            self.conversation_log = self.make_messages_from_prompt(
                self.current_answer , messages=self.conversation_log)
            
            return self.current_answer
        except Exception as e:
            return f"An error occurred while communicating with {settings['model']}: {str(e)}"
    
    def make_messages_from_prompt(self, prompt, role=None, messages=None):
        if role is None:
            role = 'user'
        if messages is None:
            messages = []
        messages.append({"role": role, "content": prompt})
        return messages

    def extract_code_from_GPT_response(self, content):
        """Extract code from GPT response."""
        try:
            code_env_helper = paths.code_executor_environment_helper_paths[self.task_api_name]
            with open(code_env_helper, 'r') as file:
                code_env_content = file.read()
        except:
            code_env_content = ""
        try:
            code = code_env_content + "\n" + content.split("```python")[1].split("```")[0]
        except:
            return None
        return code
        
    def code_executor(self, code):
        """Interpreter for code."""
        return interpreter.computer.run("python", code)[0]['content']
    
    async def serve_user_query(self, user_query):
        log_content = self.logger.get_chat_history(full=False)
        msg = self.prompt_template.default_system_prompt(user_query, log_content)
        response = await self.API_communicator(msg, **config.general_agent_settings)
        return response
    
    def find_relevant_examples(self, user_query):
        if config.cheap:
            # use RAG, cheaper option
            keys = self.retriever.search(query=user_query, k=config.NUM_CODING_EXAMPLES)
            df = pd.read_csv(paths.CODE_REFERENCE_EXAMPLE_PATH + "coding.csv")
            examples = []
            for key in keys:
                examples.append({key['content']: df['answer'].iloc[key['passage_id']]})
        else:
            # input everything, more expensive but accurate
            df = pd.read_csv(paths.CODE_REFERENCE_EXAMPLE_PATH + "coding.csv")
            examples = []
            for _, row in df.iterrows():
                example = {
                        'query': row['query'],
                        'answer': row['answer'],
                    }
                examples.append(example)
        json_examples = json.dumps(examples, indent=2)
        return str(json_examples)
    
      
