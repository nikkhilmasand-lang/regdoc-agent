import re
from typing import Dict, Any
from openai import OpenAI

from regdoc_agent.retrieval.semantic import retrieve_chunks


OBLIGATION_PATTERN = re.compile(
    r"\b(must|shall|should|required|requirement|mandatory|ensure|comply|prohibited|not allowed)\b",
    re.IGNORECASE,
)


class ExtractAgent:
    """
    Handles extraction-style queries (obligations, timelines, exceptions).

    v1 behavior:
    - Retrieve relevant evidence passages
    - Apply refusal thresholds
    - Perform lightweight rule-based extraction (no LLM)
    """

    def __init__(
        self,
        client: OpenAI,
        top_k: int = 5,
        min_top_score: float = 0.55,
        min_margin: float = 0.20,
    ):
        self.client = client
        self.top_k = top_k
        self.min_top_score = min_top_score
        self.min_margin = min_margin

    def run(self, query: str) -> Dict[str, Any]:
        results = retrieve_chunks(client=self.client, query=query, top_k=self.top_k)

        if not results:
            return {
                "ok": False,
                "reason": "No evidence retrieved from the indexed documents.",
                "top_score": None,
                "margin": None,
                "extractions": [],
                "results": results,
            }

        top_score = results[0]["score"]
        second_score = results[1]["score"] if len(results) > 1 else None
        margin = (top_score - second_score) if second_score is not None else None

        ok_by_score = top_score >= self.min_top_score
        ok_by_margin = (margin is None) or (margin >= self.min_margin)
        evidence_ok = ok_by_score and ok_by_margin

        # Lightweight extraction: find sentences with obligation language
        extractions = []
        for r in results:
            text = r.get("text_preview", "")
            if OBLIGATION_PATTERN.search(text):
                extractions.append({
                    "doc_id": r["doc_id"],
                    "chunk_id": r["chunk_id"],
                    "source_file": r["source_file"],
                    "snippet": text,
                })

        if not evidence_ok:
            return {
                "ok": False,
                "reason": "Insufficient evidence for a supported extraction (weak semantic match).",
                "top_score": top_score,
                "margin": margin,
                "extractions": extractions,
                "results": results,
            }

        # Even if semantic evidence is okay, refuse if we found no obligation statements
        if not extractions:
            return {
                "ok": False,
                "reason": "Retrieved evidence does not contain clear obligation language (e.g., must/shall/required).",
                "top_score": top_score,
                "margin": margin,
                "extractions": [],
                "results": results,
            }

        return {
            "ok": True,
            "top_score": top_score,
            "margin": margin,
            "extractions": extractions,
            "results": results,
        }
