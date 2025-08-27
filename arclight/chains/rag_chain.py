from __future__ import annotations
import os
from typing import List
from dataclasses import dataclass, asdict

# Fallback Doc type for demo mode
@dataclass
class Doc:
    source: str
    content: str

def _demo_docs(q: str) -> List[Doc]:
    return [
        Doc(source="/docs/azure_rag.pdf#p1", content="Azure AI Search enables semantic and vector retrieval."),
        Doc(source="/docs/agentic_patterns.md", content="Planner → Researcher → Reviewer reflects and retries."),
    ]

def _format_ctx(docs: List[dict]) -> str:
    return "\n\n".join([f"[{i+1}] {d.get('source')}: {d.get('content')[:700]}" for i, d in enumerate(docs)])

def _use_azure_search() -> bool:
    return all([
        os.getenv("AZURE_SEARCH_ENDPOINT"),
        os.getenv("AZURE_SEARCH_KEY"),
        os.getenv("AZURE_SEARCH_INDEX"),
    ])

def _embedder():
    from langchain_openai import AzureOpenAIEmbeddings
    return AzureOpenAIEmbeddings(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-06-01"),
        azure_deployment=os.environ["AZURE_OPENAI_EMBED_DEPLOYMENT"],
    )

def _search_azure(query: str, k: int = 6) -> List[dict]:
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents import SearchClient
    from azure.search.documents.models import Vector

    endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
    key = os.environ["AZURE_SEARCH_KEY"]
    index = os.environ["AZURE_SEARCH_INDEX"]

    sc = SearchClient(endpoint, index, AzureKeyCredential(key))
    try:
        # Try vector search first
        vec = _embedder().embed_query(query)
        results = sc.search(search_text=None, vector=Vector(value=vec, k=k, fields="embedding"),
                            select=["title", "source", "content"])
    except Exception:
        # Fallback to keyword search if vector fails
        results = sc.search(search_text=query, select=["title", "source", "content"])

    docs = []
    for r in results:
        docs.append({"title": r.get("title"), "source": r.get("source"), "content": r.get("content")})
    return docs

def retrieve_docs(query: str) -> List[Doc] | List[dict]:
    if _use_azure_search():
        return _search_azure(query)
    return _demo_docs(query)

def answer_with_context(llm, question: str, k: int = 6) -> dict:
    docs = retrieve_docs(question)
    # normalize to dicts
    if docs and hasattr(docs[0], "__dict__"):
        docs = [asdict(d) for d in docs]  # demo mode Doc -> dict
    context = _format_ctx(docs[:k])
    prompt = f"""You are a careful researcher. Use the context to answer and include citations like [1], [2].

Question: {question}

Context:
{context}
"""
    resp = llm.invoke(prompt)
    return {"answer": getattr(resp, "content", str(resp)), "docs": docs[:k], "prompt": prompt}
