from langchain_openai import ChatOpenAI
from packages.utils_func import get_token

def chat_openai(
    query : str,
    model : str = "gpt-4o-mini",
):
    llm = ChatOpenAI(
        api_key=get_token("read", "openai"),
        model=model
    )
    response = llm.invoke(query)
    return response.content