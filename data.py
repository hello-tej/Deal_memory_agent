from memory import store_memory

DEALS = {
    "acme_corp": [
        "Call 1 [Discovery]: CTO Alice raised API latency concerns. Competitor Salesforce mentioned.",
        "Call 2 [Negotiation]: CFO pushed on pricing. We countered with ROI story — engagement improved.",
        "Call 3 [Objection]: Security team asked for SOC2 report. Promised by Q3.",
        "Call 4 [Negotiation]: Discussed 10% volume discount. Waiting on legal.",
    ],
    "globex": [
        "Call 1 [Discovery]: Pricing was main objection. Led with features — lost interest.",
        "Call 2 [Negotiation]: Switched to ROI framing. Engagement jumped. Quarterly billing requested.",
        "Call 3 [Objection]: Procurement wants annual commit, not quarterly.",
    ],
    "initech": [
        "Call 1 [Discovery]: Champion Bob loves the UI. Legal review required before sign-off.",
        "Call 2 [Negotiation]: Legal asked for DPA. Sent template. Waiting.",
    ],
}

def seed_memories():
    count = 0
    for deal_id, logs in DEALS.items():
        for log in logs:
            store_memory(deal_id, log, metadata={"type": "seed", "deal": deal_id})
            count += 1
    return count