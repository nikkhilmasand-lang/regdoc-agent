import os
import json
from pathlib import Path

import numpy as np
import faiss
from dotenv import load_dotenv
from openai import OpenAI

INDEX_PATH = Path("index/faiss.index")
META_PATH = Path("index/chunk_meta.json")

EMBED_MODEL = "text-embedding-3-small"


def embed_query(client: OpenAI, text: str) -> np.ndarray:
    """Convert a user query into a normalized embedding vector."""
    resp = client.embeddings.create(model=EMBED_MODEL, input=text)
    vec = np.array(resp.data[0].embedding, dtype="float32").reshape(1, -1)
    faiss.normalize_L2(vec)  # makes dot-product behave like cosine similarity
    return vec


def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not found in .env")

    if not INDEX_PATH.exists() or not META_PATH.exists():
        raise FileNotFoundError("Index not found. Run scripts/ingest.py then scripts/build_index.py first.")

    client = OpenAI(api_key=api_key)

    index = faiss.read_index(str(INDEX_PATH))
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))

    query = input("Ask a question: ").strip()
    if not query:
        return

    q_vec = embed_query(client, query)

    # IMPORTANT FIX:
    # If you ask FAISS for more results than exist, it pads with id=-1 and score=-FLT_MAX.
    # So we cap k to index.ntotal and skip any invalid ids.
    k = min(5, index.ntotal)
    scores, ids = index.search(q_vec, k)

    print("\nTop retrieved passages:\n")

    shown = 0
    for idx, score in zip(ids[0], scores[0]):
        if idx == -1:
            continue

        m = meta[int(idx)]
        shown += 1
        print(f"{shown}. score={score:.3f}")
        print(f"   doc: {m['doc_id']} | chunk: {m['chunk_id']}")
        print(f"   source: {m['source_file']}")
        print(f"   preview: {m['text_preview']}")
        print()

    if shown == 0:
        print("No relevant passages found.")


if __name__ == "__main__":
    main()
