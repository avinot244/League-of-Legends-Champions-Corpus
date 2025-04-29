from services.prompt_provider.prompt_provider import get_prompt
from services.chat.anthropic_chat import chat_anthropic

import json

def champion_role(champion_context : str, error_path : str) -> str:
    prompt : str = get_prompt("champion_role")
    
    prompt = prompt.replace("{{CHAMPION_CONTEXT}}", champion_context)
    
    try:
        llm_output = chat_anthropic(prompt)
        champion_role_description = llm_output.split("```markdown")[1].split("```")[0]
    except Exception as e:
        print(llm_output)
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
    
    return champion_role_description