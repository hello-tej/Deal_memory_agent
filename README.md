# 🧠 DealMemory — Sales Intelligence Agent with Persistent Memory

> A sales copilot that remembers every deal interaction — objections, competitors, stakeholders, pricing — and gets smarter with each call.

Built with **[Hindsight](https://github.com/vectorize-io/hindsight)** (memory layer), **Groq** (LLM inference), and **Streamlit** (UI).

---

## 🎯 The Problem

Sales reps lose deals because they forget. Not the big things — the small, specific things:

- The CFO who pushed back on pricing three times
- The security team that asked for SOC 2 twice
- The competitor mentioned in passing on call one

All of this lives in CRM notes nobody reads before the next call. Stateless LLM agents give generic advice ("Schedule a discovery call") because they have no memory of the specific deal.

**DealMemory fixes this.** Every interaction is retained in Hindsight. Every brief is grounded in the actual deal history. Patterns emerge across calls that a human would miss.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│  Streamlit UI (app.py)              │
│  - Deal selector                    │
│  - Query input                      │
│  - Log call form                    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  Agent Layer (agent.py)             │
│  - brief_rep()  → recall + LLM      │
│  - smart_brief() → reflect          │
│  - log_call()   → retain            │
└──────┬────────────────────┬─────────┘
       │                    │
┌──────▼────────┐  ┌────────▼─────────┐
│  Hindsight    │  │  Groq LLM        │
│  (memory.py)  │  │  gpt-oss-120b    │
│  retain()     │  │  - Briefing      │
│  recall()     │  │  - Synthesis     │
│  reflect()    │  │                  │
└───────────────┘  └──────────────────┘
```

**Three layers, one job each:**
- **UI layer** — what the rep sees
- **Agent layer** — thin orchestration between memory and LLM
- **Memory layer** — Hindsight, with its own API surface (`retain`, `recall`, `reflect`)

The agent layer never touches raw LLM context. It always asks Hindsight for relevant memories first, then hands grounded context to Groq.

---

## 🔑 How Hindsight Memory Is Used

Hindsight is not a bolt-on feature. It **is** the product. Without it, the agent is a generic chatbot.

### 1. `retain()` — Store every interaction

Each deal has its own memory bank (`acme_corp`, `globex`, `initech`). Every call log is retained:

```python
from memory import store_memory

store_memory(
    bank_id="acme_corp",
    content="Call 2 [Negotiation]: CFO pushed on pricing. We countered with ROI story — engagement improved.",
    metadata={"type": "call_log", "outcome": "Negotiation"}
)
```

Bank auto-creates on the first `retain()`. No explicit setup.

### 2. `recall()` — Retrieve relevant memories

When a rep asks for a brief, the agent queries Hindsight:

```python
from memory import recall_memories

memories = recall_memories("acme_corp", "What objections have been raised?")
# → List[RecallResult] with .text attribute
```

Each memory has a `.text` attribute — the raw content that gets joined into LLM context.

### 3. `reflect()` — AI-synthesized answers

Beyond recall, Hindsight's `reflect()` synthesizes memories into a strategic recommendation:

```python
from memory import reflect_on_deal

recommendation = reflect_on_deal("acme_corp", "What should I do next?")
# → "Based on 5 calls, the CFO has a pricing sensitivity pattern — every pushback was neutralized by an ROI story. Recommended next action: send updated proposal with SSO + ROI framing."
```

Recall gives you a list. **Reflect gives you a decision.**

---

## ⚡ The Before/After Moment

**Query:** "Brief me on Acme Corp."

### Without memory:
> "Schedule a discovery call. Confirm the stakeholder map. Document objections early."

### With memory (after 5 logged calls):
> "Based on prior interactions with Acme Corp:
> - **Stakeholder:** Alice (CTO) raised API latency concerns
> - **Objection pattern:** CFO pushed on pricing 3× — ROI framing shifted him to agreement every time
> - **Competitor:** Salesforce named during discovery, still on the radar
> - **Open items:** SOC 2 report promised by Q3 2026; 10% volume discount pending legal
> - **Next best action:** Send updated proposal with SSO + ROI framing. Push legal on discount. Follow up on SOC 2 delivery this week."

The LLM didn't get smarter. **The context did.**

---

## 🚀 Setup & Run

### Prerequisites
- Python 3.10+
- Hindsight Cloud account ([get free credits](https://ui.hindsight.vectorize.io) — promo code `MEMHACK99`)
- Groq API key ([free tier](https://console.groq.com))

### Installation

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/https://github.com/hello-tej/Deal_memory_agent.git
cd dealmemory

# Virtual environment
python -m venv .venv
source .venv/bin/activate    # Windows: .\.venv\Scripts\Activate

# Dependencies
pip install -r requirements.txt
```

### Environment Setup

Create `.env` in the project root:

```env
HINDSIGHT_API_KEY=your_hindsight_key
HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io
GROQ_API_KEY=your_groq_key
```

### Run

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 🎬 Demo Flow

1. Click **"🌱 Seed Initial Data"** — populates Hindsight with synthetic deal history (3 deals, 9 calls)
2. Select **`acme_corp`** from the dropdown
3. Click **"⚡ Quick Brief (Groq + Recall)"** — agent recalls specific objections, competitors, and open items
4. Log a new call via the **"📝 Log New Call"** form
5. Click **"⚡ Quick Brief"** again — the new memory is immediately incorporated
6. Click **"🧠 Deep Brief (Hindsight Reflect)"** — AI-synthesized strategic recommendation

Watch the agent go from **generic → specific → pattern-aware** across interactions.

---

## 📁 Project Structure

```
dealmemory/
├── app.py              # Streamlit UI
├── agent.py            # LLM orchestration (Groq)
├── memory.py           # Hindsight client wrapper
├── data.py             # Synthetic deal data
├── pyt.py              # Debug/recall test script
├── requirements.txt    # Dependencies
├── .env                # API keys (not committed)
├── .gitignore
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Tool | Why |
|---|---|---|
| Memory | [Hindsight](https://hindsight.vectorize.io/) | Clean retain/recall/reflect primitives |
| LLM | [Groq](https://groq.com/) (`openai/gpt-oss-120b`) | Sub-second inference, generous free tier |
| UI | [Streamlit](https://streamlit.io/) | Fast demo iteration |
| Language | Python 3.10+ | Hindsight SDK native |

---

## 💡 Design Decisions

**1. Bank-per-deal.** Each deal gets its own Hindsight bank. Recall is scoped by default — Acme's objections never contaminate Globex's brief.

**2. Memory goes in the user message, not system.** Memories are data, not instructions. Keeping them separate from the persona preserves the distinction between "who you are" and "what happened."

**3. Async indexing handled explicitly.** Hindsight retains are asynchronous (1-3 sec). The `log_call()` flow includes a `wait_for_index(2)` to ensure the memory is searchable before the next brief.

**4. Reflect is the killer feature.** Most memory layers stop at recall. Hindsight's `reflect()` turns a pile of memories into a coherent recommendation. That's the difference between a search engine and a copilot.

---

## 📚 Resources

- [Hindsight GitHub](https://github.com/vectorize-io/hindsight)
- [Hindsight Documentation](https://hindsight.vectorize.io/)
- [What Is Agent Memory?](https://vectorize.io/what-is-agent-memory)

---

## 👥 Team

Built by **Team DealMemory**:

- **Parella Tejguru** — Team Lead, Architecture
- **Akshith Bijjigiri** — LLM & Groq Integration
- **Pooja Boddula** — Pattern Detection
- **Bhargavi Cheera** — UX & Demo Design
- **Lakshmi Niharika Kattam** — Synthetic Data
- **Snehitha Namani** — Reflect & AI Synthesis

---

## 📄 License

MIT
