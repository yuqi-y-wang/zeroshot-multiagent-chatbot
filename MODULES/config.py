OPENAI_API_KEY = ""
ANTHROPIC_API_KEY = ""
FIREWORKS_API_KEY = ""

coding_settings_openai = {
    "model": "gpt-4o",
    "temperature": 0,
}
chat_settings_openai = {
    "model": "gpt-3.5-turbo",
    "temperature": 0,
}
cheap_setting_openai = {
    "model": "gpt-4o-mini-2024-07-18",
    "temperature": 0,
}
coding_settings_anthropic = {
    "model": "claude-3-5-sonnet-20240620",
    "max_tokens": 2048,
}
llama_settings_fireworks = {
    "model": "accounts/fireworks/models/llama-v3p1-405b-instruct",
    "max_tokens": 1024,
    "temperature": 0,
}
# llama_settings_fireworks = {
#     "model": "accounts/fireworks/models/llama-v3p1-70b-instruct",
#     "max_tokens": 1024,
# }
# llama_settings_fireworks = {
#     "model": "accounts/fireworks/models/llama-v3p1-8b-instruct",
#     "max_tokens": 1024,
# }

price_dict = {
    "input":{
        "gpt-4o": 5,
        "gpt-4o-mini-2024-07-18": 0.15,
        "claude-3-5-sonnet-20240620": 3,
        "gpt-3.5-turbo": 0.5,
        "accounts/fireworks/models/llama-v3p1-8b-instruct": 0.2,
        "accounts/fireworks/models/llama-v3p1-70b-instruct": 0.9,
        "accounts/fireworks/models/llama-v3p1-405b-instruct": 3,
    },
    "output":{
        "gpt-4o": 15,
        "gpt-4o-mini-2024-07-18": 0.6,
        "claude-3-5-sonnet-20240620": 15,
        "gpt-3.5-turbo": 1.5,
        "accounts/fireworks/models/llama-v3p1-8b-instruct": 0.2,
        "accounts/fireworks/models/llama-v3p1-70b-instruct": 0.9,
        "accounts/fireworks/models/llama-v3p1-405b-instruct": 3,
    }
}

## Doorman agent
task_assigner_settings = coding_settings_anthropic
final_answer_settings = coding_settings_anthropic
## general agents
general_agent_settings = cheap_setting_openai
## nantum agents
nantum_agent_settings = cheap_setting_openai
## coding agents
mv_agent_settings = coding_settings_anthropic
raw_data_retriever_agent_settings = coding_settings_anthropic
compliance_agent_settings = coding_settings_anthropic

NUM_CODING_EXAMPLES = 3
NUM_NANTUM_EXAMPLES = 3

cheap = True