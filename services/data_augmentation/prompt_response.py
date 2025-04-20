from services.prompt_provider.prompt_provider import get_prompt
from services.chat.anthropic_chat import chat_anthropic
import json



def prompt_response(context : str, n : int) -> list[str]:
    """
    Generate a response based on the given context using a language model.

    Args:
        context (str): The context for generating the response.
        n (int): The number of responses to generate.

    Returns:
        list[dict]: A list of dictionaries containing the generated responses.
    """
    prompt : str = get_prompt("prompt_response")
    
    prompt_ = prompt.replace("{{CONTEXT}}", context)
    prompt_ = prompt_.replace("{{N}}", str(n))
    
    llm_output = chat_anthropic(prompt_)
    
    # Extract the generated responses from the output
    qa_pairs : list[dict] = []
    print(llm_output)
    
    try:
        data = json.loads(llm_output.split("```json")[1].split("```")[0])
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return []
    for qa_pair in data:
        qa_pairs.append(qa_pair)
    
    return qa_pairs