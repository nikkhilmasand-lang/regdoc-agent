import sys
import os
from pathlib import Path

# Allow imports from src/
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from dotenv import load_dotenv
from openai import OpenAI

from regdoc_agent.agents.lookup import LookupAgent


def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not found in environment")

    client = OpenAI(api_key=api_key)
    agent = LookupAgent(client)

    query = input("Ask a question: ").strip()
    if not query:
        print("No query provided.")
        return

    results = agent.run(query)

    if not results:
        print("\nNo relevant passages found.\n")
        return

    print("\nTop retrieved passages:\n")
    for i, r in enumerate(results, start=1):
        print(f"{i}. score={r['score']:.3f}")
        print(f"   doc: {r['doc_id']} | chunk: {r['chunk_id']}")
        print(f"   source: {r['source_file']}")
        print(f"   preview: {r['text_preview']}")
        print()


if __name__ == "__main__":
    main()
