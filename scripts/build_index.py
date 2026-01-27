import os
import json
from pathlib import Path

import numpy as np
import faiss
from dotenv import load_dotenv
from openai import OpenAI

CHUNKS_PATH = Path("data/processed/chunks.jsonl")
INDEX_PATH = Path("index/faiss.index")
META_PATH = Path("index/chunk_meta.json")

EMBED_MODEL = "text-embedding-3-small"  # good + cost-effective


def load_chunks():
    chunks = []
    with CHUNKS_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            chunks.append(json.loads(line))
    return chunks


def embed_batch(client: OpenAI, texts: list[str]) -> np.ndarray:
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    vecs = [d.embedding for d in resp.data]
    return np.array(vecs, dtype="float32")


def main():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not found. Put it in .env at repo root.")

    if not CHUNKS_PATH.exists():
        raise FileNotFoundError(f"Missing {CHUNKS_PATH}. Run scripts/ingest.py first.")

    client = OpenAI(api_key=api_key)
    chunks = load_chunks()
    if not chunks:
        raise RuntimeError("No chunks found. Check data/processed/chunks.jsonl.")

    texts = [c["text"] for c in chunks]
    print(f"Embedding {len(texts)} chunks using {EMBED_MODEL}...")

    # Embed in small batches (safe for bigger corpora later)
    BATCH = 64
    all_vecs = []
    for i in range(0, len(texts), BATCH):
        batch = texts[i : i + BATCH]
        vecs = embed_batch(client, batch)
        all_vecs.append(vecs)
        print(f"  embedded {min(i + BATCH, len(texts))}/{len(texts)}")

    vectors = np.vstack(all_vecs)

    # Normalize so dot-product behaves like cosine similarity
    faiss.normalize_L2(vectors)

    dim = vectors.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(vectors)

    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(INDEX_PATH))

    # Save metadata: FAISS row id -> chunk info
    # ✅ CHANGE: store full chunk text as well, so ExtractAgent can do real extraction.
    meta = []
    for c in chunks:
        full_text = c["text"]
        preview = full_text.replace("\n", " ").strip()[:280]

        meta.append({
            "doc_id": c["doc_id"],
            "chunk_id": c["chunk_id"],
            "source_file": c["source_file"],
            "text_preview": preview,
            "text": full_text,  # ✅ NEW: full chunk text (not just preview)
        })

    META_PATH.parent.mkdir(parents=True, exist_ok=True)
    META_PATH.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✅ Saved FAISS index: {INDEX_PATH}")
    print(f"✅ Saved metadata map: {META_PATH}")


if __name__ == "__main__":
    main()
