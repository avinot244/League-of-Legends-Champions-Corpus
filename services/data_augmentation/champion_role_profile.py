from services.prompt_provider.prompt_provider import get_prompt
from services.chat.anthropic_chat import chat_anthropic
import json

def champion_role_profile(id : str, champion_name: str, ability_description: str, error_path : str) -> str:
    
    """
    Generate a role profile for a given champion based on their abilities.

    Args:
        champion_name (str): The name of the champion.
        ability_description (str): The description of the champion's abilities.

    Returns:
        str: The generated role profile.
    """
    prompt: str = get_prompt("champion_card")
    
    prompt = prompt.replace("{{CHAMPION_NAME}}", champion_name)
    prompt = prompt.replace("{{ABILITY_DESCRIPTIONS}}", ability_description)
    llm_output = chat_anthropic(prompt)
    try:
        role_profile = llm_output.split("<champion_card>")[1].split("</champion_card>")[0]
    except IndexError:
        try:
            with open(error_path, "r") as file:
                error_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            error_data = {"ids": []}

        # Add the id to the list of ids
        if "ids" not in error_data:
            error_data["ids"] = []
        error_data["ids"].append(id)

        # Save the updated error data back to the JSON file
        with open(error_path, "w") as file:
            json.dump(error_data, file, indent=4)

        return None
        
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
