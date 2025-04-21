from langchain_anthropic import ChatAnthropic
from packages.utils_func import get_token



def chat_anthropic(
    query : str,
    model : str = "claude-3-5-haiku-20241022",
    temperature : float = 0.7,
    streaming : bool = False,
):
    """
    Function to interact with the Anthropic API using the ChatAnthropic class.
    
    Args:
        query (str): The input query to send to the model.
        model (str): The model to use. Default is "claude-3-5-haiku-20241022".
        temperature (float): The temperature for the model's response. Default is 0.7.
        stream (bool): Whether to stream the response. Default is False.
    
    Returns:
        str: The model's response.
    """
    # Initialize the ChatAnthropic object
    llm = ChatAnthropic(
        api_key=get_token("read", "anthropic"),
        model=model,
        temperature=temperature,
        streaming=streaming,
        max_tokens=5000,
    )

    # Get the response from the model
    response = llm.invoke(query)
    return response.content


