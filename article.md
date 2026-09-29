# How I Designed a Sales Agent That Actually Remembers Every Deal

**By Parella Tejguru**

Sales reps lose deals for a stupid reason: they forget. Not the big things — the small, specific things. The CFO who pushed back on pricing three times. The security team that asked for SOC 2 twice. The competitor mentioned in passing on call one. All of this lives somewhere in a CRM note that no one reads before the next call.

I spent a weekend building a fix. Not a chatbot. A memory-first sales copilot that compounds context across every interaction with a deal.

This is the story of how I designed the architecture, why memory had to be the product and not a feature, and the three design decisions that made it work.

## The problem with stateless sales agents

Every LLM demo I've seen for sales looks the same. You type a company name, the agent gives you generic advice:

> "Schedule a discovery call. Confirm the stakeholder map. Document objections early."

That's not useless — but it's also not worth paying for. Any sales rep can Google a discovery call checklist.

What's actually valuable is knowing **this specific deal**. That Acme Corp's CFO has a pattern of raising pricing objections and only responding to ROI framing. That the security team is a hard gate. That Salesforce is the competitor and they're winning on compliance messaging.

That knowledge only exists in memory. And memory only exists if you architect for it.

## The architecture: three layers, one job each

I split the system into three layers so that memory, reasoning, and UI stay independent. Here's what the stack looks like:




The key insight: **the agent layer never touches raw LLM context directly.** It always asks Hindsight for relevant memories first, then hands a grounded context block to the LLM.

## Why Hindsight, not a vector database

I could have built this with Pinecone and a bunch of glue code. Instead I used [Hindsight](https://github.com/vectorize-io/hindsight) because it gives me three distinct primitives I'd otherwise have to build myself:

1. **`retain()`** — store a memory in a named bank
2. **`recall()`** — retrieve relevant memories by query
3. **`reflect()`** — synthesize an answer from memories using the memory layer's own reasoning

That third one is the killer. Most memory layers stop at recall. Hindsight's `reflect()` turns a pile of memories into a coherent answer. That's the difference between "here are 20 things that happened" and "here's the pattern and what to do next."

The full [Hindsight documentation](https://hindsight.vectorize.io/) covers this, but the [agent memory primer](https://vectorize.io/what-is-agent-memory) is what actually convinced me memory needed to be architecturally separate from the LLM.


The key insight: **the agent layer never touches raw LLM context directly.** It always asks Hindsight for relevant memories first, then hands a grounded context block to the LLM.

## Why Hindsight, not a vector database

I could have built this with Pinecone and a bunch of glue code. Instead I used [Hindsight](https://github.com/vectorize-io/hindsight) because it gives me three distinct primitives I'd otherwise have to build myself:

1. **`retain()`** — store a memory in a named bank
2. **`recall()`** — retrieve relevant memories by query
3. **`reflect()`** — synthesize an answer from memories using the memory layer's own reasoning

That third one is the killer. Most memory layers stop at recall. Hindsight's `reflect()` turns a pile of memories into a coherent answer. That's the difference between "here are 20 things that happened" and "here's the pattern and what to do next."

The full [Hindsight documentation](https://hindsight.vectorize.io/) covers this, but the [agent memory primer](https://vectorize.io/what-is-agent-memory) is what actually convinced me memory needed to be architecturally separate from the LLM.

## The memory layer, in ~30 lines

The entire memory wrapper is small enough to read in one sitting:

```python
# memory.py
import os, time
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
    try:
        response = client.recall(bank_id=bank_id, query=query, budget=budget)
        return getattr(response, "results", None) or []
    except Exception as e:
        print(f"[recall_memories ERROR] bank={bank_id} | {e}")
        return []

def reflect_on_deal(bank_id: str, query: str):
    try:
        response = client.reflect(bank_id=bank_id, query=query)
        return getattr(response, "text", str(response))
    except Exception as e:
        return "Unable to generate reflection."