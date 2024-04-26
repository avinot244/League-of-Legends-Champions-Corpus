import re

def replace_within_double_curly_brackets(text):
    # Regular expression to find substrings within double curly braces
    pattern = r'{{(.*?)}}'

    # Find all matches
    matches = re.findall(pattern, text)

    # Replace each match with its last character
    for match in matches:
        last_char = match[-1] if match else ''
        text = text.replace('{{' + match + '}}', last_char)

    return text

# Example usage
input_text = "{{championSpells.AatroxQ}} some other text {{anotherExample.YourSpell}}"
output_text = replace_within_double_curly_brackets(input_text)
print(output_text)