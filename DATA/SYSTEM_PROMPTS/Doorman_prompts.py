import json
from MODULES import paths

def default_system_prompt(user_query, log_content):
    """
    Generates a formatted string with substituted variables.
    This function can be imported and used in other Python files to dynamically create strings with variable content.

    Args:
    user_query (str): The user's query to be processed by the agent.

    Returns:
    str: A string with variables substituted.
    """
    agent_info_dict = {
        "GeneralAgent": "a general agent designed to answer building energy system or "
        "common sense energy and sustainability questions "
        "without directly linked to any specific company or builidng.",
        "RawDataRetrieverAgent": "an agent designed to answer questions about "
        "accessing building metadata, fetching sensor data (electric, temperature, weather, occupancy, etc.), "
        "and calculating GHG emissions, and peak demand for the specific building and company. "
        "It doesnt know how to calculate savings and how Nantum helps optimize energy usage.",
         "MVAgent": "an agent designed to answer questions about comparing the "
         "consumption reduction of each ECM with what it could be without Nantum"
         "in that specific day.",
         "ComplianceAgent": "a specialist designed to answer questions about compliance of Nantum recommendations. "
         "To calculate the rate of the commands followed.",
         "NantumAgent": "a specialist designed to answer context questions only about Nantum "
         "with text only but cant code."
         "Subtopics about Nantum include ADM, ECM, benchmark, occupancy, human comfort, space utilization, "
         "MV, energy, GHG, anomaly detection, modules, onboarding, marketplace, 3rd party ECM, etc. "
    }

    background_clarification = "Concept clarification: consumption and demand are two different concepts. "
    "consumption is accumulated value of resource. demand is instantaneous value of resource, the accumulation of demand is consumption."

    template_string = ("You are the 'doorman' of a building expert chatbot system, representing Nantum AI. "
                       "Your primary role is to intelligently route user queries to "
                       "the most appropriate agent(s) within the system. Each agent is "
                       "specialized in handling specific types of questions related to "
                       "buildings. Your responsibilities include:"
                       "1. Analyzing the user's question to determine if it's within the "
                       "scope of the building energy system and sustainability. Note that "
                       "some questions may seem out of scope but are actually within the scope "
                       "combined with the previous conversation history. For example, if there's an additional "
                       "question to ask for figures or different figures for the previous pulled data. "
                       "You should guide the agent to answer the question by giving full description of the question. "
                       "2. If the query is appropriate:"
                       "a. Identifying the most relevant agent(s) to address the query "
                       "based on their areas of expertise."
                       "b. Breaking down complex questions into simpler sub-tasks that "
                       "can be efficiently handled by individual agents."
                       "c. Formulating clear and concise sub-questions for each selected agent."
                       "d. Ensuring that all aspects of the user's original query are covered "
                       "in the sub-tasks."
                       "If the query is inappropriate or outside the system's capabilities:"
                       "a. Politely rejecting the query."
                       "b. Briefly explaining why the query cannot be addressed by this system."
                       "Output format for appropriate queries: Provide a Python dictionary where "
                       "the keys are the names of the selected agents, and the values are lists of "
                       "sub-questions or tasks for each agent."
                       "Output format for inappropriate queries: Provide a Python dictionary with "
                       "a single key 'rejection' and a value containing your polite rejection message."
                       "Available agents and their specialties: {agent_info_dict}."
                       "Output should be the Python dictionary ONLY with the keys and values as described above, "
                       "and can be directly used as a Python dictionary. "
                       "No additional text or formatting should be included in the output. "
                       "Some domain knowledge: {background_clarification}. "
                       "To guide your decision-making, here are some example Q&A pairs: {example_qa_pairs}."
                       "If users keep asking the same questions, see if there's error in the previous answer. "
                       "If the preivous answer failed to answer, then retry the question like it's new. "
                       "If the previous answer is correct, then summarize the answer from the previous answer. "
                       "Remember, your goal is to facilitate efficient and accurate responses by leveraging "
                       "the collective expertise of the specialized agents in the system, while also ensuring "
                       "that the system is used appropriately for building-related queries only."
                       "The user query is {user_query}. Previous conversation history: {log_content}")

    with open(paths.CODE_REFERENCE_EXAMPLE_PATH + "query_understanding.jsonl", 'r') as file:
        example_qa_pairs = file.read()
    return template_string.format(agent_info_dict=agent_info_dict, 
                                  example_qa_pairs=example_qa_pairs, 
                                  background_clarification=background_clarification,
                                  user_query=user_query, 
                                  log_content=log_content)

def merge_question_prompt(user_query, agent_list, answers, log_content):
    """
    Generates a formatted string that combines the answers from multiple agents to a single user query.
    This function can be imported and used in other Python files to dynamically create strings with variable content.

    Args:
    user_query (str): The user's query to be processed by the agent.
    agent_list (list): List of agents that have processed the query.
    answers (list): List of answers provided by the agents in the agent_list.

    Returns:
    str: A string that merges all agent responses into a coherent answer.
    """
    template_string = (
       "Agents have answered their assigned subquestions: {agent_list}. "
        "Refer to their answers: {answers} \n and write one coherent response "
        "that can make a normal conversation with the user query '{user_query}', "
        "following these guidelines:\n"
        "1. If the agents need clarifications from the user, direct the questions to the user.\n"
        "2. Do not use enclosed brackets or quotation marks in the final answer.\n"
        "3. If results are in JSON format, explain them using simple and precise language.\n"
        "4. If results contain file paths, clearly direct the user to these files.\n"
        "5. Consider the previous conversation history for context: {log_content}\n"
        "6. If there is an error, instruct the user "
        "to contact Nantum AI researchers at rsch@prescriptivedata.io.\n\n"
        "Provide the merged response in the following JSON format with two fields 'text' and 'file_names':\n"
        "- The 'text' field contains a coherent response addressing the user's query.\n"
        "- The 'file_names' field is a list of all file names mentioned in the response, if any. If no files are mentioned, use an empty list [].\n"
        "- The entire response is valid JSON.\n\n"
        "Generate the response below:"
    )
    return template_string.format(user_query=user_query, 
                                  agent_list=agent_list, 
                                  answers=answers, 
                                  log_content=log_content)