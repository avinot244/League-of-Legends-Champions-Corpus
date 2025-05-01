from langchain_anthropic import ChatAnthropic
from packages.utils_func import get_token
import anthropic

def chat_anthropic(
    query : str,
    model : str = "claude-3-5-haiku-20241022",
    temperature : float = 0.7,
    streaming : bool = False,
    pre_filled_response : str = None
):
    client = anthropic.Anthropic(
        api_key=get_token("read", "anthropic")
    )
    
    if pre_filled_response:
    
        messages = [
            {"role": "user", "content": query},
            {"role": "assistant", "content": pre_filled_response}
        ]
        
        message = client.messages.create(
            model=model,
            max_tokens=8000,
            temperature=temperature,
            stream=streaming,
            messages=messages
        )
        
        return message.content[0].text
 
    else:
        llm = ChatAnthropic(
            api_key=get_token("read", "anthropic"),
            model=model,
            temperature=temperature,
            streaming=streaming,
            max_tokens=8000,
        )

        # Get the response from the model
        response = llm.invoke(query)
        return response.content

