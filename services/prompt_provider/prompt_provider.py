import yaml
import os
from packages.types import t_data_type

def get_prompt(data_type : t_data_type):
    """
    Fetches the appropriate prompt for the given data_type from prompts.yml.

    Args:
        data_type (t_data_type): The type of data for which the prompt is needed.

    Returns:
        str: The corresponding prompt if found, otherwise None.
    """
    prompts_file_path = os.path.join(os.path.dirname(__file__), '../../data/prompts/prompts.yml')
    
    try:
        with open(prompts_file_path, 'r') as file:
            prompts = yaml.safe_load(file)
        for prompt in prompts:
            if list(prompt.keys())[0] == data_type:
                return prompt[data_type]
        return prompts.get(data_type, None)
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompts file not found at {prompts_file_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file: {e}")