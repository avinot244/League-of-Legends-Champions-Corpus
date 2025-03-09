from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field
from packages.utils_func import get_token

class ExtractSchema(BaseModel):
    champion_name : str
    champion_first_ability_name : str
    champion_first_ability_details : str
    champion_second_ability_name : str
    champion_second_ability_details : str
    champion_third_ability_name : str
    champion_third_ability_details : str
    champion_fourth_ability_name : str
    champion_fourth_ability_details : str
    champion_fifth_ability_name : str
    champion_fifth_ability_details : str

def extract(url : str):
    token = get_token("read", "firecrawl")
    app = FirecrawlApp(api_key=token)
    
    data = app.scrape_url(url, {
        'formats': ["json"],
        'jsonOptions': {
            'schema': ExtractSchema.model_json_schema()
        }
    })
    
    return data["json"]
    

def scrape(url : str):
    token = get_token("read", "firecrawl")
    app = FirecrawlApp(api_key=token)
    
    scrape_result = app.scrape_url(url, params={'formats': ['markdown']})
    return scrape_result["markdown"]