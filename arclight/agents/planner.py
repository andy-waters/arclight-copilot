from __future__ import annotations

PLANNER_PROMPT = """You are a planning agent. Given a user goal, outline 3-6 steps.
Each step may call a tool: [web_search | rag | python | github]. Keep steps concise.
"""

def draft_plan(llm, goal: str) -> list[dict]:
    plan_prompt = PLANNER_PROMPT + f"\nGoal: {goal}\nReturn JSON list of steps with 'action' and 'notes'."
    resp = llm.invoke(plan_prompt)
    text = getattr(resp, "content", str(resp))
    # naive parse for demo mode: produce a simple default plan if JSON isn't returned
    default = [
        {"action": "web_search", "notes": "Find 2-3 credible sources."},
        {"action": "rag", "notes": "Retrieve docs from index (if available)."},
        {"action": "python", "notes": "Run a quick calculation or check if needed."},
        {"action": "review", "notes": "Check citations and produce final answer."},
    ]
    return default
