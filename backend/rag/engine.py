"""
RAG Engine: Chunking → Embeddings → FAISS Index → Semantic Search
"""
import numpy as np
from typing import List, Dict, Any

_model = None
_index = None
_chunks = []

CHUNK_SIZE = 300
CHUNK_OVERLAP = 50
TOP_K = 3


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def _chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]).strip())
        if end == len(words):
            break
        start += chunk_size - overlap
    return chunks


def build_index(documents: List[Dict[str, Any]]) -> None:
    import faiss
    global _index, _chunks

    _chunks = []
    model = _get_model()

    for doc in documents:
        for i, chunk in enumerate(_chunk_text(doc["content"])):
            _chunks.append({
                "chunk_id": f"{doc['id']}_chunk_{i}",
                "doc_id": doc["id"],
                "title": doc["title"],
                "content": chunk,
                "chunk_index": i,
            })

    texts = [c["content"] for c in _chunks]
    embeddings = model.encode(texts, show_progress_bar=False, normalize_embeddings=True)
    embeddings_array = np.array(embeddings, dtype=np.float32)

    dim = embeddings_array.shape[1]
    _index = faiss.IndexFlatIP(dim)
    _index.add(embeddings_array)
    print(f"[RAG] Indexed {len(_chunks)} chunks from {len(documents)} documents.")


def search(query: str, top_k: int = TOP_K) -> List[Dict[str, Any]]:
    if _index is None or not _chunks:
        raise RuntimeError("RAG index not built. Call build_index() first.")

    model = _get_model()
    query_array = np.array(
        model.encode([query], normalize_embeddings=True),
        dtype=np.float32
    )
    scores, indices = _index.search(query_array, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if 0 <= idx < len(_chunks):
            chunk = _chunks[idx].copy()
            chunk["similarity_score"] = float(score)
            results.append(chunk)
    return results


def format_context(retrieved_chunks: List[Dict[str, Any]]) -> str:
    return "\n\n".join(
        f"[Source {i}: {c['title']}]\n{c['content']}"
        for i, c in enumerate(retrieved_chunks, 1)
    )
