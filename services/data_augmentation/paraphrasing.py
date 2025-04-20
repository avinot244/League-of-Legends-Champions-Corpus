from services.prompt_provider.prompt_provider import get_prompt
from services.chat.anthropic_chat import chat_anthropic


def paraphrase_text(text : str) -> str:
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
    paraphrased_text = llm_output.split("<paraphrased_text>")[1].split("</paraphrased_text>")[0]
    return paraphrased_text