from services.prompt_provider.prompt_provider import get_prompt
from services.chat.anthropic_chat import chat_anthropic
import json

def role_instruct(context : str, nb_pairs : int, error_path : str, id : str) -> list[dict]:
    prompt : str = get_prompt("instruct_role")
    prompt = prompt.replace("{{CONTEXT}}", context)
    prompt = prompt.replace("{{N}}", str(nb_pairs))
    
    try:
        llm_output = chat_anthropic(prompt)
        qa_pairs = llm_output.split("<output>")[1].split("</output>")[0]
        return json.loads(qa_pairs)
    except Exception as e:
        print(e)
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