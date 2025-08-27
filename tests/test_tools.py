from arclight.tools.web_search import web_search
from arclight.tools.py_sandbox import run_snippet

def test_web_search_stub():
    res = web_search("agentic ai")
    assert isinstance(res, list) and len(res) >= 1
    assert hasattr(res[0], "title")

def test_sandbox_ok():
    out = run_snippet("x=1+2")
    assert out["ok"] and out["result"]["x"] == 3

def test_sandbox_err():
    out = run_snippet("import os")  # not allowed
    assert not out["ok"]
