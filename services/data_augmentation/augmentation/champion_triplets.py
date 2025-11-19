from services.prompt_provider.prompt_provider import get_prompt
from services.chat.anthropic_chat import chat_anthropic
from services.chat.openai_chat import chat_openai

from typing import Literal

import json

def champion_triplets(
    anchor_description: str,
    positive_description: str,
    negative_description: str,
    index: int,
    nb_triplets : int = 3,
    llm_provider : Literal["anthropic", "openai"] = "anthropic",
    model_name: str = None
) -> list[dict]:
    prompt = get_prompt("champion_triplets_short")
    prompt = prompt.replace("{{ANCHOR_DESCRIPTION}}", anchor_description)
    prompt = prompt.replace("{{POSITIVE_DESCRIPTION}}", positive_description)
    prompt = prompt.replace("{{NEGATIVE_DESCRIPTION}}", negative_description)
    prompt = prompt.replace("{{NUM_TRIPLETS}}", str(nb_triplets))
    
    
    if llm_provider == "anthropic":
        if model_name is not None:
            llm_output : str = chat_anthropic(prompt, model=model_name)
        llm_output : str = chat_anthropic(prompt, model="claude-haiku-4-5-20251001")
    elif llm_provider == "openai":
        if model_name is not None:
            llm_output : str = chat_openai(prompt, model=model_name)
        llm_output : str = chat_openai(prompt, model="gpt-4.1-mini")
    
        
        
    try:
        json_output = llm_output.split("```json")[1].strip().split("```")[0]
        triplets = json.loads(json_output)
        return triplets
    except Exception as e:
        print(f"{index} : Error generating champion triplets: {e} ")

#392
#574