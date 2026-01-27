import os
import json
from pathlib import Path

import tiktoken

RAW_DIR = Path("data/raw")
OUT_PATH = Path("data/processed/chunks.jsonl")

# Simple chunking parameters (good enough for v1)
MODEL_ENCODING = "cl100k_base"
CHUNK_TOKENS = 220
OVERLAP_TOKENS = 40

def chunk_text(text: str, doc_id: str):
    enc = tiktoken.get_encoding(MODEL_ENCODING)
    tokens = enc.encode(text)

    chunks = []
    start = 0
    chunk_id = 0

    # Safety: prevent infinite loops
    prev_start = -1

    while start < len(tokens):
        if start == prev_start:
            # If we aren't moving forward, break to avoid infinite loop
            break
        prev_start = start

        end = min(start + CHUNK_TOKENS, len(tokens))
        chunk_tokens = tokens[start:end]
        chunk_txt = enc.decode(chunk_tokens).strip()

        if chunk_txt:
            chunks.append({
                "doc_id": doc_id,
                "chunk_id": chunk_id,
                "text": chunk_txt,
            })
            chunk_id += 1

        # If we've reached the end, stop
        if end >= len(tokens):
            break

        # Move window forward with overlap
        start = max(0, end - OVERLAP_TOKENS)

    return chunks

def main():
    if not RAW_DIR.exists():
        raise FileNotFoundError(f"Missing {RAW_DIR}. Create it and add .txt files.")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    total = 0
    with OUT_PATH.open("w", encoding="utf-8") as f_out:
        for fp in sorted(RAW_DIR.glob("*.txt")):
            doc_id = fp.stem
            text = fp.read_text(encoding="utf-8", errors="ignore").strip()
            if not text:
                continue

            chunks = chunk_text(text, doc_id)
            for c in chunks:
                # minimal metadata for now; we’ll expand later
                c["source_file"] = str(fp)
                f_out.write(json.dumps(c, ensure_ascii=False) + "\n")
                total += 1

    print(f"✅ Wrote {total} chunks to {OUT_PATH}")

if __name__ == "__main__":
    main()
