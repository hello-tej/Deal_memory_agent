import os
import time
from hindsight_client import Hindsight
from dotenv import load_dotenv

load_dotenv()

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

def store_memory(bank_id: str, content: str, metadata: dict = None):
    try:
        return client.retain(
            bank_id=bank_id,
            content=content,
            metadata=metadata or {"type": "call_log"}
        )
    except Exception as e:
        print(f"[store_memory ERROR] bank={bank_id} | {e}")
        return None

def recall_memories(bank_id: str, query: str, budget: str = "mid"):
    """Returns a list of RecallResult objects with .text attribute."""
    try:
        response = client.recall(bank_id=bank_id, query=query, budget=budget)
        # RecallResponse object — .results is list of RecallResult
        results = getattr(response, "results", None) or []
        return results
    except Exception as e:
        print(f"[recall_memories ERROR] bank={bank_id} | {e}")
        return []

def reflect_on_deal(bank_id: str, query: str):
    try:
        response = client.reflect(bank_id=bank_id, query=query)
        return getattr(response, "text", str(response))
    except Exception as e:
        print(f"[reflect ERROR] bank={bank_id} | {e}")
        return "Unable to generate reflection."

def wait_for_index(seconds: int = 2):
    time.sleep(seconds)