from services.prompt_provider.prompt_provider import get_prompt
from services.chat.anthropic_chat import chat_anthropic
import json

def json2markdown(json_text : str, error_path : str) -> list[dict]:
    prompt : str = get_prompt("json2markdown")
    
    prompt = prompt.replace("{{CHAMPION_JSON}}", json_text)
    
    llm_output = chat_anthropic(prompt)
    
    try:
        md_text = llm_output.split("<markdown>")[1].split("</markdown>")[0]
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
    
    return md_text