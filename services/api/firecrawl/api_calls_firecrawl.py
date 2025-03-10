from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field
from packages.utils_func import get_token

import json

def get_schema() -> dict:
    data : dict = dict
    with open("./model_firecrawl.json", "r") as f:
        data = json.load(f)
        
    return data

def extract(url : str):
    token = get_token("read", "firecrawl")
    app = FirecrawlApp(api_key=token)
    
    data = app.scrape_url(url, {
        'formats': ["json"],
        'jsonOptions': {
            'schema': get_schema()
        }
    })
    
    return data["json"]
    

def scrape(url : str):
    token = get_token("read", "firecrawl")
    app = FirecrawlApp(api_key=token)
    
    scrape_result = app.scrape_url(url, params={'formats': ['markdown']})
    return scrape_result["markdown"]