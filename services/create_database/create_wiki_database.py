from services.api.firecrawl.api_calls_firecrawl import scrape

def create_wiki_database():
    result = scrape("")
    encoded_result = result.encode("utf-8")
    print(encoded_result.decode("utf-8"))