from firecrawl import FirecrawlApp
import json
from pydantic import BaseModel

from packages.utils_func import get_token
from services.api.firecrawl.model_provider import model_provider

def extract(url : str):
    token = get_token("read", "firecrawl")
    app = FirecrawlApp(api_key=token)
    
    model = model_provider(url)    
    data = app.extract([url], {
        "schema": model.model_json_schema()
    })
    
    return data["data"]
    

def scrape(url : str):
    token = get_token("read", "firecrawl")
    app = FirecrawlApp(api_key=token)
    
    scrape_result = app.scrape_url(url, params={'formats': ['markdown']})
    return scrape_result["markdown"]