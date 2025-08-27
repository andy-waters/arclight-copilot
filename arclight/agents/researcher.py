from __future__ import annotations
from arclight.tools.web_search import web_search
from arclight.chains.rag_chain import answer_with_context


def execute_step(llm, step: dict, question: str, log: list[dict]) -> None:
    action = step.get("action", "")
    if action == "web_search":
        results = web_search(question)
        log.append({"step": action, "result": [r.__dict__ for r in results]})
    elif action == "rag":
        out = answer_with_context(llm, question)
        log.append({"step": action, "result": out})
    elif action == "python":
        # no-op in demo unless user supplies code; handled in UI panel
        log.append({"step": action, "result": "Ready for code snippet (optional)."})
    else:
        log.append({"step": action or "noop", "result": "No action taken."})
