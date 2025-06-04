from services.prompt_provider.prompt_provider import get_prompt
from services.chat.anthropic_chat import chat_anthropic

import json

def generate_champion_features(champion_description : str) -> dict:
    prompt : str = get_prompt("champion_feature_analysis")
    
    prompt = prompt.replace("{{CHAMPION_ABILITY_DESCRIPTION}}", champion_description)
    llm_output = chat_anthropic(prompt)
    
    try:
        champion_features = llm_output.split("<json_output>")[1].split("</json_output>")[0]
    except Exception as e:
        print(e)
        
    return json.loads(champion_features)["associations"]