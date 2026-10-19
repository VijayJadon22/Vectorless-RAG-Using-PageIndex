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
result = pi_client.submit_document(PDF_PATH)
doc_id = result["doc_id"]

print("Uploaded")
print(f"Doc ID: {doc_id}")

# ── Poll until processing is complete ───────────────────────────────────────
# PageIndex builds the tree asynchronously.
# For a 50-page PDF this typically takes 30–90 seconds.

print("⏳ Building tree index...")
print("   (This runs once per document — the index is cached for reuse)")

while True:
    status_result = pi_client.get_document(doc_id)
    status = status_result.get("status")
    print(f"   Status: {status}")

    if status == "completed":
        print("\n✅ Tree index ready!")
        break
    elif status == "failed":
        print("\n❌ Processing failed. Check your PDF format.")
        break

    time.sleep(5)


# Fetch the full tree
tree_result = pi_client.get_tree(doc_id, node_summary=True)
pageindex_tree = tree_result.get("result", [])

print(f"📊 Top-level sections: {len(pageindex_tree)}")
print("\n🌲 Raw tree (first node):")
print(json.dumps(pageindex_tree[0] if pageindex_tree else {}, indent=2))


# ── Pretty-print the full tree ───────────────────────────────────────────────


def print_tree(nodes, indent=0):
    """Recursively print tree titles for a visual overview."""
    for node in nodes:
        prefix = "  " * indent + ("└─ " if indent > 0 else "")
        page = node.get("page_index", "?")
        print(f"{prefix}[{node['node_id']}] {node['title']}  (p.{page})")
        if node.get("nodes"):
            print_tree(node["nodes"], indent + 1)


print("📚 Full Document Structure:\n")
print_tree(pageindex_tree)


# ── Count total nodes ────────────────────────────────────────────────────────
def count_nodes(nodes):
    total = len(nodes)
    for n in nodes:
        if n.get("nodes"):
            total += count_nodes(n["nodes"])
    return total

total = count_nodes(pageindex_tree)
print(f"🔢 Total nodes in tree: {total}")
print("   Each node = one retrievable section of the document")