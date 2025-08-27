# arclight/memory/conversation_store.py
from __future__ import annotations

import dataclasses
import datetime
import json
import pathlib
import time

STORE = pathlib.Path(".arclight_store.json")


def _to_jsonable(obj):
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    if isinstance(obj, (set,)):
        return list(obj)
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    return str(obj)


def append_trace(entry: dict) -> None:
    data = []
    if STORE.exists():
        try:
            data = json.loads(STORE.read_text(encoding="utf-8"))
        except Exception:
            data = []
    entry = {"ts": int(time.time()), **entry}
    STORE.write_text(
        json.dumps([*data, entry], indent=2, default=_to_jsonable), encoding="utf-8"
    )


def export_trace() -> str:
    if STORE.exists():
        return STORE.read_text(encoding="utf-8")
    return "[]"
