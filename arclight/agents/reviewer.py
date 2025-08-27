from __future__ import annotations

def review_and_finalize(llm, question: str, log: list[dict]) -> dict:
    context_bits = []
    for entry in log:
        if entry.get("step") == "rag" and isinstance(entry.get("result"), dict):
            ans = entry["result"].get("answer", "")
            context_bits.append(ans)
    review_prompt = f"""You are a strict reviewer.
Ensure the answer is concise, cites sources like [1], [2], and avoids speculation.
Question: {question}
Draft fragments:
{chr(10).join(context_bits[:2])}

Return the final answer.
"""
    resp = llm.invoke(review_prompt)
    return {"final": getattr(resp, "content", str(resp))}
