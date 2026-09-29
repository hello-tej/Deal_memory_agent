import os
from dotenv import load_dotenv
load_dotenv()

print("BASE URL:", os.getenv("HINDSIGHT_BASE_URL"))
print("API KEY (first 10):", os.getenv("HINDSIGHT_API_KEY", "")[:10])

from hindsight_client import Hindsight
client = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

# Recall test on existing bank
result = client.recall(bank_id="acme_corp", query="What concerns were raised?")
print("RECALL RAW:", result)
print("TYPE:", type(result))