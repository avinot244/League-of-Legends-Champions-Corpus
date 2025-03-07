from firecrawl import FirecrawlApp
from packages.utils_func import get_token

def scrape(url : str):
    token = get_token("read", "firecrawl")
    app = FirecrawlApp(api_key=token)
    
    scrape_result = app.scrape_url('https://wiki.leagueoflegends.com/en-us/Thresh', params={'formats': ['markdown']})
    return scrape_result["markdown"]