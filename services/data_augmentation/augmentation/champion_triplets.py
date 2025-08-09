from services.prompt_provider.prompt_provider import get_prompt
from services.chat.anthropic_chat import chat_anthropic

from anthropic._exceptions import OverloadedError
import time

import json

def champion_triplets(
    anchor_description: str,
    positive_description: str,
    negative_description: str,
    index: int,
    nb_triplets : int = 5,
) -> list[dict]:
    prompt = get_prompt("champion_triplets")
    prompt = prompt.replace("{{ANCHOR_DESCRIPTION}}", anchor_description)
    prompt = prompt.replace("{{POSITIVE_DESCRIPTION}}", positive_description)
    prompt = prompt.replace("{{NEGATIVE_DESCRIPTION}}", negative_description)
    prompt = prompt.replace("{{NUM_TRIPLETS}}", str(nb_triplets))
    
    
    try:
        llm_output : str = chat_anthropic(prompt, model="claude-3-5-sonnet-20241022")
    except OverloadedError as o:
        print(f"{index} : Overload of AnthropicAPI")
        time.sleep(300)
        
        
    try:
        json_output = llm_output.split("```json")[1].strip().split("```")[0]
        triplets = json.loads(json_output)
        return triplets
    except Exception as e:
        print(f"{index} : Error generating champion triplets: {e} ")

#392
#574