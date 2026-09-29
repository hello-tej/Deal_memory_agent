import streamlit as st
from agent import brief_rep, smart_brief, log_call
from data import DEALS, seed_memories

st.set_page_config(page_title="DealMemory", page_icon="🧠", layout="wide")
st.title("🧠 DealMemory — Sales Copilot")
st.caption("A sales agent with persistent memory across every deal interaction.")

deal_id = st.selectbox("Select Deal", list(DEALS.keys()))

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🌱 Seed Initial Data"):
        n = seed_memories()
        st.success(f"Seeded {n} memories across {len(DEALS)} deals.")

# --- Brief Section ---
st.subheader("📋 Pre-Call Brief")
query = st.text_input("Ask about this deal", "Brief me on the current status")

c1, c2 = st.columns(2)
with c1:
    if st.button("⚡ Quick Brief (Groq + Recall)"):
        with st.spinner("Recalling memories..."):
            st.write(brief_rep(deal_id, query))
with c2:
    if st.button("🧠 Deep Brief (Hindsight Reflect)"):
        with st.spinner("Synthesizing..."):
            st.write(smart_brief(deal_id, query))

# --- Log Section ---
st.divider()
st.subheader("📝 Log New Call")
notes = st.text_area("Call Notes", placeholder="What happened? Objections? Competitors? Next steps?")
outcome = st.selectbox("Outcome", ["Discovery", "Negotiation", "Objection", "Closed-Won", "Closed-Lost"])
if st.button("💾 Log Call to Memory"):
    msg = log_call(deal_id, notes, outcome)
    st.success(msg)