import sys
import os
from pathlib import Path

# Allow imports from src/
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from dotenv import load_dotenv
from openai import OpenAI

from regdoc_agent.orchestrator.router import Orchestrator


def _print_obligations(exts):
    print("\nExtracted obligations (rule-based):\n")
    for i, e in enumerate(exts, start=1):
        category = e.get("category", "General")
        obligation = e.get("obligation", "").strip()
        print(f"{i}. [{category}] {obligation}")
        print(f"   source: {e.get('doc_id')} | chunk: {e.get('chunk_id')} | {e.get('source_file')}")
        print()


def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not found in environment")

    client = OpenAI(api_key=api_key)
    orchestrator = Orchestrator(client)

    query = input("Ask a question: ").strip()
    if not query:
        print("No query provided.")
        return

    out = orchestrator.run(query)

    intent = out.get("intent", "unknown")
    print(f"\nIntent: {intent}")

    if not out.get("ok", False):
        print("\nREFUSAL")
        print(f"- reason: {out.get('reason', 'Insufficient evidence.')}")

        if out.get("top_score") is not None:
            print(f"- top_score: {out['top_score']:.3f}")
        else:
            print("- top_score: N/A")

        if out.get("margin") is not None:
            print(f"- margin: {out['margin']:.3f}")

        # Show extractions if present (even on refusal, for transparency)
        if intent == "extract":
            exts = out.get("extractions", [])
            if exts:
                _print_obligations(exts)
            else:
                print("\nNo obligation-like statements detected in retrieved evidence.\n")

        if not out.get("results"):
            print("No passages retrieved.")
            return

        print("Closest retrieved passages (for transparency):\n")

    else:
        print("\nOK")

        if out.get("top_score") is not None:
            print(f"- top_score: {out['top_score']:.3f}")

        if out.get("margin") is not None:
            print(f"- margin: {out['margin']:.3f}")

        if intent == "extract":
            exts = out.get("extractions", [])
            if exts:
                _print_obligations(exts)
            else:
                print("\nNo obligation-like statements detected in retrieved evidence.\n")

        print("\nTop retrieved passages:\n")

    for i, r in enumerate(out.get("results", []), start=1):
        print(f"{i}. score={r['score']:.3f}")
        print(f"   doc: {r['doc_id']} | chunk: {r['chunk_id']}")
        print(f"   source: {r['source_file']}")
        print(f"   preview: {r.get('text_preview', '')}")
        print()


if __name__ == "__main__":
    main()
