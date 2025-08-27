from __future__ import annotations
import os, uuid, glob, re
from dataclasses import dataclass
from typing import Iterable, List

from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, SimpleField, SearchableField, SearchField, SearchFieldDataType,
    VectorSearch, HnswAlgorithmConfiguration, VectorSearchProfile, CorsOptions, Suggester
)
from azure.search.documents import SearchClient
from azure.search.documents.models import Vector

# LangChain embeddings (Azure)
from langchain_openai import AzureOpenAIEmbeddings

SEARCH_ENDPOINT = os.environ["AZURE_SEARCH_ENDPOINT"]
SEARCH_KEY = os.environ["AZURE_SEARCH_KEY"]
INDEX_NAME = os.environ.get("AZURE_SEARCH_INDEX", "arclight-docs")

AOAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
AOAI_KEY = os.environ["AZURE_OPENAI_API_KEY"]
AOAI_API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-06-01")
EMBED_DEPLOY = os.environ["AZURE_OPENAI_EMBED_DEPLOYMENT"]  # text-embedding-3-small

EMBED_DIM = 1536  # text-embedding-3-small dimension

def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def _chunks(text: str, size: int = 1200, overlap: int = 200) -> Iterable[str]:
    text = re.sub(r"\s+\n", "\n", text).strip()
    start = 0
    while start < len(text):
        end = min(len(text), start + size)
        yield text[start:end]
        if end == len(text): break
        start = max(end - overlap, start + 1)

def ensure_index():
    sic = SearchIndexClient(SEARCH_ENDPOINT, AzureKeyCredential(SEARCH_KEY))

    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="title", type=SearchFieldDataType.String, sortable=True, filterable=True, analyzer_name="en.lucene"),
        SearchableField(name="content", type=SearchFieldDataType.String, analyzer_name="en.lucene"),
        SimpleField(name="source", type=SearchFieldDataType.String, filterable=True),
        SearchField(
            name="embedding",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            vector_search_dimensions=EMBED_DIM,
            vector_search_profile_name="vprofile"
        ),
        SearchableField(name="tags", type=SearchFieldDataType.Collection(SearchFieldDataType.String), filterable=True, facetable=True),
    ]

    index = SearchIndex(
        name=INDEX_NAME,
        fields=fields,
        cors_options=CorsOptions(allowed_origins=["*"], max_age_in_seconds=60),
        suggesters=[Suggester(name="sg", source_fields=["title", "content"])],
        vector_search=VectorSearch(
            algorithms=[HnswAlgorithmConfiguration(name="hnsw")],
            profiles=[VectorSearchProfile(name="vprofile", algorithm_configuration_name="hnsw")],
        ),
    )
    sic.create_or_update_index(index)

def build_embedder():
    return AzureOpenAIEmbeddings(
        azure_endpoint=AOAI_ENDPOINT,
        api_key=AOAI_KEY,
        api_version=AOAI_API_VERSION,
        azure_deployment=EMBED_DEPLOY,
    )

def gather_docs(content_dir: str = "content") -> List[dict]:
    doc_paths = glob.glob(f"{content_dir}/**/*.md", recursive=True) + glob.glob(f"{content_dir}/**/*.txt", recursive=True)
    docs: List[dict] = []
    for path in doc_paths:
        raw = _read_text(path)
        title = path.split("/")[-1].replace(".md", "").replace(".txt", "")
        for i, chunk in enumerate(_chunks(raw)):
            docs.append({
                "id": f"{path}#chunk-{i}-{uuid.uuid4().hex[:8]}",
                "title": title,
                "content": chunk,
                "source": path,
                "tags": [p for p in path.split("/") if p not in ("content", "")]
            })
    return docs

def embed_and_upload(docs: List[dict]):
    sc = SearchClient(SEARCH_ENDPOINT, INDEX_NAME, AzureKeyCredential(SEARCH_KEY))
    embedder = build_embedder()

    texts = [d["content"] for d in docs]
    vectors = embedder.embed_documents(texts)
    for d, v in zip(docs, vectors):
        d["embedding"] = v

    # Upload in batches
    batch = []
    for d in docs:
        batch.append(d)
        if len(batch) == 1000:
            sc.upload_documents(batch); batch = []
    if batch:
        sc.upload_documents(batch)

if __name__ == "__main__":
    ensure_index()
    docs = gather_docs("content")
    if not docs:
        print("No docs found under ./content — add a few Markdown files and re-run.")
    else:
        embed_and_upload(docs)
        print(f"Indexed {len(docs)} chunks into '{INDEX_NAME}'.")
