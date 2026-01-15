import json
from pathlib import Path
from typing import List, Dict

import numpy as np
import faiss
from openai import OpenAI

INDEX_PATH = Path("index/faiss.index")
META_PATH = Path("index/chunk_meta.json")
EMBED_MODEL = "text-embedding-3-small"


def retrieve_chunks(client: OpenAI, query: str, top_k: int = 5) -> List[Dict]:
    """
    Retrieve top-k semantically relevant document chunks for a query.

    Returns a list of dicts with:
      - doc_id
      - chunk_id
      - source_file
      - text_preview
      - score
    """
    if not INDEX_PATH.exists() or not META_PATH.exists():
        raise FileNotFoundError("FAISS index or metadata not found. Run build_index first.")

    index = faiss.read_index(str(INDEX_PATH))
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))

    # Embed query
    resp = client.embeddings.create(model=EMBED_MODEL, input=query)
    q_vec = np.array(resp.data[0].embedding, dtype="float32").reshape(1, -1)
    faiss.normalize_L2(q_vec)

    k = min(top_k, index.ntotal)
    scores, ids = index.search(q_vec, k)

    results = []
    for idx, score in zip(ids[0], scores[0]):
        if idx == -1:
            continue

        m = meta[int(idx)]
        results.append({
            "doc_id": m["doc_id"],
            "chunk_id": m["chunk_id"],
            "source_file": m["source_file"],
            "text_preview": m["text_preview"],
            "score": float(score),
        })

    return results
