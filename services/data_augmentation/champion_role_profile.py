from services.prompt_provider.prompt_provider import get_prompt
from services.chat.anthropic_chat import chat_anthropic
import json

def champion_role_profile(champion_name: str, ability_description: str) -> str:
    
    """
    Generate a role profile for a given champion based on their abilities.

    Args:
        champion_name (str): The name of the champion.
        ability_description (str): The description of the champion's abilities.

    Returns:
        str: The generated role profile.
    """
    prompt: str = get_prompt("champion_card")
    
    prompt_ = prompt.replace("{{CHAMPION_NAME}}", champion_name)
    prompt_ = prompt_.replace("{{ABILITY_DESCRIPTION}}", ability_description)
    
    llm_output = chat_anthropic(prompt_)
    role_profile = llm_output.split("<champion_card>")[1].split("</champion_card>")[0]
    
    return role_profile

def get_list_id() -> list[str]:
    id_list : list[str] = []
    
    with open("./data/fill-mask/v6/wiki_data_chunks_champions.jsonl", "r") as f1, open("./data/fill-mask/v6/wiki_data_str_champions-enhenced.jsonl", "r") as f2:
        for (line1, line2) in zip(f1, f2):
            data1 = json.loads(line1)
            data2 = json.loads(line2)
            if not(data1["id"] in id_list):
                id_list.append(data1["id"])
            
            if not(data2["id"] in id_list):
                id_list.append(data2["id"])
    return id_list
