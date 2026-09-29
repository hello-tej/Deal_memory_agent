import os
from groq import Groq
from memory import store_memory, recall_memories, reflect_on_deal, wait_for_index

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are DealMemory, a sales intelligence copilot with persistent memory.
When briefing a rep:
- Cite SPECIFIC past objections, competitors, stakeholders, and outcomes
- Highlight patterns (e.g., "pricing objection raised twice, ROI framing worked both times")
- Suggest the next best action based on what worked before
- Be concise. No fluff. Reps are busy."""

def brief_rep(deal_id: str, query: str) -> str:
    """Recall + LLM brief."""
    memories = recall_memories(deal_id, query)

    # ✅ FIX: use .text not .content
    context_str = "\n".join([m.text for m in memories]) if memories else "No relevant history."

    user_prompt = f"""DEAL HISTORY:
{context_str}

REP QUERY: {query}

Give a specific, memory-grounded brief. Cite concrete past details."""

    try:
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            model="openai/gpt-oss-120b",
            temperature=0.6,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[Groq Error] {e}"

def smart_brief(deal_id: str, query: str) -> str:
    """Uses Hindsight reflect() — AI synthesis."""
    return reflect_on_deal(deal_id, query)

def log_call(deal_id: str, notes: str, outcome: str) -> str:
    content = f"[{outcome}] {notes}"
    store_memory(deal_id, content, metadata={"type": "call_log", "outcome": outcome})
    wait_for_index(2)
    return f"Logged for {deal_id}. Memory indexed."