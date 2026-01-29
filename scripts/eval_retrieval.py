import os
import sys
import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# ---- PATH FIX (IMPORTANT) ----
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.append(str(SRC))
# ------------------------------

from regdoc_agent.retrieval.semantic import retrieve_chunks

EVAL_PATH = Path("data/eval/eval_questions.json")
TOP_K = 3


def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not found")

    client = OpenAI(api_key=api_key)

    if not EVAL_PATH.exists():
        raise FileNotFoundError(f"Missing eval file: {EVAL_PATH}")

    eval_data = json.loads(EVAL_PATH.read_text(encoding="utf-8"))

    hits = 0
    evaluated = 0

    print("\nRunning retrieval evaluation\n" + "-" * 32)

    for item in eval_data:
        question = item["question"]
        expected_doc = item["expected_doc"]

        results = retrieve_chunks(client, question, top_k=TOP_K)
        retrieved_docs = [r["doc_id"] for r in results]

        evaluated += 1

        if expected_doc and expected_doc in retrieved_docs:
            hits += 1
            status = "✅ HIT"
        elif expected_doc is None:
            status = "⚠️ EXPECTED REFUSAL"
        else:
            status = "❌ MISS"

        print(f"\nQ: {question}")
        print(f"Expected: {expected_doc}")
        print(f"Retrieved: {retrieved_docs}")
        print(f"Result: {status}")

    print("\nSummary")
    print("-------")
    print(f"Evaluated: {evaluated}")
    print(f"Hits: {hits}")
    print(f"Precision@{TOP_K}: {hits / evaluated:.2f}")


if __name__ == "__main__":
    main()
