from MODULES import paths
from MODULES.utils import summarize_ipynb

def default_system_prompt(input, log_content, examples):
    """
    Generates a formatted string with substituted variables.
    This function can be imported and used in other Python files to dynamically create strings with variable content.

    Args:
    input (str): The user's question or input string.
    log_content (str): The log of previous conversation history.

    Returns:
    str: A string with variables substituted into a template.
    """
    simple_examples = paths.code_example_paths['compliance']
    simple_examples = summarize_ipynb(simple_examples)
    # with open(paths.CODE_REFERENCE_EXAMPLE_PATH + "coding.jsonl", 'r') as file:
    #     examples = file.read()
    with open(paths.CODE_REFERENCE_DOCUMENT_PATH + "function_specs.txt", 'r') as file:
        function_specs = file.read()
    
    template_string = (
        "As a compliance agent representing Nantum AI, your role is to assist users "
        "by writing Python code to retrieve, analyze, and visualize compliance-relevant data. "
        "This includes calculating the number of accepted recommendations and compliance rates. "
        "Follow these guidelines:\n\n"
        "1. Make sure you know building and company name from the user's input instead of from the following examples."
        "2. No extra output than coding. Write executable Python code enclosed in a single block: ```python\n<code>\n```\n"
        "3. Save the complete DataFrame to a file if the data is long "
        "and print both the data and the file path.\n"
        "4. Trying including data visualization code, save the figure, "
        "and print the figure file path as well. Barplots are more preferred. Do not use pie charts unless specified by users. "
        "Make sure the xticks are clearly visible and the figure is readable. "
        "For example, the xticks should only keep the month and day if the data is daily; "
        "the xticks should only keep the hour if the data is hourly within a day, etc. \n "
        "5. Ensure your code is efficient, well-commented, and follows best practices.\n"
        "6. If additional libraries are needed, include import statements.\n\n"
        "Simple examples of usage: {simple_examples}\n\n"
        "Always follow the examples instead of improvising. Examples of previous interactions: {examples}\n\n"
        "Function input/output specifications and some context information: {function_specs}\n\n"
        "Previous conversation history: {log_content}\n\n"
        "User's current question: {content}\n\n"
        "Respond with appropriate Python code to address the user's question."
        "If clarification is needed, do not write code. "
        "Ask the user for more details instead and output the clarification only."
    )

    return template_string.format(content=input, 
                                  simple_examples=simple_examples, 
                                  function_specs=function_specs, 
                                  examples=examples, 
                                  log_content=log_content)
