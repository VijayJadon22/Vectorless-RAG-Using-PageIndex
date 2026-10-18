from dotenv import load_dotenv
import os, json, time
from pageindex import PageIndexClient
from langchain.chat_models import init_chat_model
from pathlib import Path

load_dotenv()

pi_client = PageIndexClient(api_key=os.getenv("PAGEINDEX_API_KEY"))
llm = init_chat_model(
    "gemini-3.5-flash-lite",
    model_provider="google_genai",
    api_key=os.getenv("GEMINI_API_KEY"),
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PDF_PATH = PROJECT_ROOT / "data" / "React.pdf"

print(f"Uploading PDF: {PDF_PATH}")
result=pi_client.submit_document(PDF_PATH)
doc_id=result['doc_id']

print("Uploaded")
print(f"Doc ID: {doc_id}")