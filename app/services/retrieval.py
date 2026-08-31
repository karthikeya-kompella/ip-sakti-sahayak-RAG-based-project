# app/services/retrieval.py
from app.db.chroma_client import collection
from app.services.embedding import embed_texts

def retrieve_chunks(query: str, regime: str, top_k: int = 5) -> list[dict]:
    query_embedding = embed_texts([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={"regime": regime},
    )

    chunks = []
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    for doc_text, meta in zip(documents, metadatas):
        chunks.append({
            "chunk_text": doc_text,
            "title": meta.get("title"),
            "language": meta.get("language"),
            "doc_type": meta.get("doc_type"),
            "source_url": meta.get("source_url"),
        })

    return chunks