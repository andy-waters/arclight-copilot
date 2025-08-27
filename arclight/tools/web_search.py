from __future__ import annotations
from dataclasses import dataclass

# NOTE: This is a stub for CI/demo. Swap in Tavily/SerpAPI for real search.
# Return a few canned results to demonstrate the agent log & citations.


@dataclass
class WebResult:
    title: str
    url: str
    snippet: str


def web_search(query: str) -> list[WebResult]:
    demo = [
        WebResult(
            title="Agentic Workflows Overview",
            url="https://example.com/agentic",
            snippet="Primer on planning, tool use, and reflection.",
        ),
        WebResult(
            title="RAG with Azure AI Search",
            url="https://example.com/azure-rag",
            snippet="Indexing and retrieval patterns with Azure Search.",
        ),
        WebResult(
            title="LangChain Tools Guide",
            url="https://example.com/langchain-tools",
            snippet="How to build tools and agents.",
        ),
    ]
    return demo
