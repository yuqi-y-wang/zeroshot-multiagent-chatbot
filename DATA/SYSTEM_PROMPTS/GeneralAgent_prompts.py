def default_system_prompt(user_query, log_content):
    """
    Generates a formatted string with substituted variables.
    This function can be imported and used in other Python files to dynamically create strings with variable content.

    Args:
    user_query (str): The user's query to be processed by the agent.

    Returns:
    str: A string with variables substituted.
    """

    template_string = ("You are a building energy and control system expert chatbot. "
                        "If you don't know for sure, output 'I'm still learning'."
                       "User query: {content}. Previous conversation history: {log_content}"
                       # "Here are some additional references about each agent: {references}. "
                      )
    return template_string.format(content=user_query, log_content=log_content)
