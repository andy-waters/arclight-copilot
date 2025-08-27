from __future__ import annotations

# Extremely restricted Python 'sandbox' for quick calculations.
# In a real deployment, use a proper isolated service or runner.

ALLOWED_BUILTINS = {"len": len, "sum": sum, "min": min, "max": max, "range": range}

def run_snippet(code: str) -> dict:
    local_env = {}
    try:
        exec(code, {"__builtins__": ALLOWED_BUILTINS}, local_env)
        return {"ok": True, "result": {k: v for k, v in local_env.items() if not k.startswith("_")}}
    except Exception as e:
        return {"ok": False, "error": str(e)}
