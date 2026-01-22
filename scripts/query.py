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
    - Run Orchestrator (intent routing)
    - Print OK or REFUSAL with evidence (and extract snippets when available)
    """

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

        # For extract intent, still show if any obligation-like snippets were detected
        if intent == "extract":
            exts = out.get("extractions", [])
            if exts:
                print("\nExtracted obligation-like statements (partial, rule-based):\n")
                for i, e in enumerate(exts, start=1):
                    print(f"{i}. doc: {e['doc_id']} | chunk: {e['chunk_id']} | source: {e['source_file']}")
                    print(f"   snippet: {e['snippet']}")
                    print()
            else:
                print("\nNo obligation-like statements detected in retrieved evidence.\n")

        # If no retrieved passages, stop
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

        # For extract intent, print extracted obligation-like snippets first
        if intent == "extract":
            exts = out.get("extractions", [])
            if exts:
                print("\nExtracted obligation-like statements (partial, rule-based):\n")
                for i, e in enumerate(exts, start=1):
                    print(f"{i}. doc: {e['doc_id']} | chunk: {e['chunk_id']} | source: {e['source_file']}")
                    print(f"   snippet: {e['snippet']}")
                    print()
            else:
                print("\nNo obligation-like statements detected in retrieved evidence.\n")

        print("\nTop retrieved passages:\n")

    for i, r in enumerate(out.get("results", []), start=1):
        print(f"{i}. score={r['score']:.3f}")
        print(f"   doc: {r['doc_id']} | chunk: {r['chunk_id']}")
        print(f"   source: {r['source_file']}")
        print(f"   preview: {r['text_preview']}")
        print()


if __name__ == "__main__":
    main()
