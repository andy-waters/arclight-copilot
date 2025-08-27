from __future__ import annotations
from arclight.config import SETTINGS
try:
    from langchain_openai import AzureChatOpenAI
except Exception:
    AzureChatOpenAI = None

class OfflineLLM:
    def invoke(self, prompt, **_):
        class R:
            def __init__(self, content): self.content = content
        return R(content="[Demo Mode] Configure Azure OpenAI for live output.\n\nPrompt excerpt: " + (prompt if isinstance(prompt, str) else str(prompt))[:400])

def azure_llm(temperature: float = 0.2, max_tokens: int = 1200):
    if SETTINGS.demo_mode or AzureChatOpenAI is None:
        return OfflineLLM()
    return AzureChatOpenAI(
        azure_deployment=SETTINGS.aoai_deployment,
        azure_endpoint=SETTINGS.aoai_endpoint,
        openai_api_version=SETTINGS.aoai_api_version,
        api_key=SETTINGS.aoai_key,
        temperature=temperature,
        max_tokens=max_tokens,
    )
