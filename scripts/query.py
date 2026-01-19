import sys
import os
from pathlib import Path

# Allow imports from src/
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from dotenv import load_dotenv
from openai import OpenAI

from regdoc_agent.orchestrator.router import Orchestrator

def main():
    """
    CLI entrypoint for querying the RegDoc Agent.

    Flow:
    - Load environment variables
    - Initialize OpenAI client
    - Run LookupAgent
    - Print OK or REFUSAL with evidence
    """

    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not found in environment")

    client = OpenAI(api_key=api_key)

    # Thresholds are intentionally conservative for regulated behavior
    orchestrator = Orchestrator(client)

    query = input("Ask a question: ").strip()
    if not query:
        print("No query provided.")
        return

    out = orchestrator.run(query)

    if not out["ok"]:
        print("\nREFUSAL")
        print(f"- reason: {out['reason']}")

        if out.get("top_score") is not None:
            print(f"- top_score: {out['top_score']:.3f}")
        else:
            print("- top_score: N/A")

        if out.get("margin") is not None:
            print(f"- margin: {out['margin']:.3f}")

        if not out["results"]:
            print("\nNo passages retrieved.\n")
            return

        print("\nClosest retrieved passages (for transparency):\n")

    else:
        print("\nOK")
        print(f"- top_score: {out['top_score']:.3f}")

        if out.get("margin") is not None:
            print(f"- margin: {out['margin']:.3f}")

        print("\nTop retrieved passages:\n")

    for i, r in enumerate(out["results"], start=1):
        print(f"{i}. score={r['score']:.3f}")
        print(f"   doc: {r['doc_id']} | chunk: {r['chunk_id']}")
        print(f"   source: {r['source_file']}")
        print(f"   preview: {r['text_preview']}")
        print()


if __name__ == "__main__":
    main()
