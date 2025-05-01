from services.prompt_provider.prompt_provider import get_prompt
from services.chat.anthropic_chat import chat_anthropic
import json

def champion_matchup(target_champion : str, champion_mechanics : str, champion_profile : str, counter_tips : str, error_path : str) -> list[dict]:
    prompt : str = get_prompt("matchup")
    
    prompt = prompt.replace("{{TARGET_CHAMPION}}", target_champion)
    prompt = prompt.replace("{{CHAMPION_MECHANICS}}", champion_mechanics)
    prompt = prompt.replace("{{CHAMPION_PROFILE}}", champion_profile)
    prompt = prompt.replace("{{COUNTER_TIPS}}", counter_tips)
    llm_output = chat_anthropic(prompt)
    
    try:
        matchup_tips = llm_output.split("<counter_strategies>")[1].split("</counter_strategies>")[0]
    except Exception as e:
        print(e)
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
    
    return json.loads(matchup_tips)