from services.prompt_provider.prompt_provider import get_prompt
from services.chat.anthropic_chat import chat_anthropic
import json


def paraphrase_text(id : str, text : str, error_path) -> str:
    """
    Paraphrase the given text using a language model.

    Args:
        text (str): The text to be paraphrased.

    Returns:
        str: The paraphrased text.
    """
    prompt : str = get_prompt("paraphrase")
    
    prompt_ = prompt.replace("{{ORIGINAL_TEXT}}", text)
    llm_output = chat_anthropic(prompt_)
    if "<paraphrased_text>" in llm_output:
        paraphrased_text = llm_output.split("<paraphrased_text>")[1].split("</paraphrased_text>")[0]
        return paraphrased_text
    elif "<papahrased_text>" in llm_output:
        paraphrased_text = llm_output.split("<papahrased_text>")[1].split("</papahrased_text>")[0]
        return paraphrased_text
    else:
        # Load the existing error data from the JSON file
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
    