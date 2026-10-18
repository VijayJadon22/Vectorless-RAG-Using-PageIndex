from dotenv import load_dotenv
import os, json, time
from pageindex import PageIndexClient
from langchain.chat_models import init_chat_model

load_dotenv()

pi_client = PageIndexClient(api_key=os.getenv("PAGEINDEX_API_KEY"))
llm = init_chat_model(
    "gemini-3.5-flash-lite",
    model_provider="google_genai",
    api_key=os.getenv("GEMINI_API_KEY"),
)

