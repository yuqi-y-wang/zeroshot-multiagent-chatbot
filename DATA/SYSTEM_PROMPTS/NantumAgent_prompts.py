def default_system_prompt(user_query, log_content):
    """
    Generates a formatted string with substituted variables.
    This function can be imported and used in other Python files to dynamically create strings with variable content.

    Args:
    user_query (str): The user's query to be processed by the agent.
    log_content (str): The log of previous conversations.

    Returns:
    str: A string with variables substituted.
    """

    template_string = "User query: {content}. Previous conversation history: {log_content}"
    return template_string.format(content=user_query, log_content=log_content)

def nantum_agent_system_prompt(user_query, log_content, references):
    """
    Generates a formatted string with substituted variables.
    This function can be imported and used in other Python files to dynamically create strings with variable content.

    Args:
    user_query (str): The user's query to be processed by the agent.
    log_content (str): The log of previous conversations.

    Returns:
    str: A string with variables substituted.
    """
    template_string = (
        "User query: {content}. Previous conversation history: {log_content}. "
        "Additional references from documents: {references}. "
    )
                       
    return template_string.format(
        content=user_query, 
        log_content=log_content,
        references=references)