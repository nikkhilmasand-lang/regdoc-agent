import re
from typing import Dict, Any, List
from openai import OpenAI

from regdoc_agent.retrieval.semantic import retrieve_chunks


OBLIGATION_PATTERN = re.compile(
    r"\b(must|shall|should|required|requirement|mandatory|ensure|comply|prohibited|not allowed)\b",
    re.IGNORECASE,
)

CATEGORY_KEYWORDS = {
    "Access Control": ["access", "role", "authorize", "privilege", "least privilege"],
    "Encryption": ["encrypt", "encryption", "keys", "cryptographic", "cipher", "rotate"],
    "Logging & Monitoring": ["log", "audit", "monitor", "alert", "retained", "retain"],
    "Incident Response": ["incident", "report", "detection", "response", "review"],
}


def guess_category(text: str) -> str:
    t = text.lower()
    for cat, kws in CATEGORY_KEYWORDS.items():
        if any(k in t for k in kws):
            return cat
    return "General"


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

    def _split_statements(self, text: str) -> List[str]:
        """
        Deterministic splitting into 'statements' for rule-based extraction.
        Keeps it simple and robust for v1.
        """
        # Normalize whitespace
        t = text.replace("\n", " ").strip()

        # Split on sentence boundaries OR bullet separators
        parts = re.split(r"(?<=[.!?])\s+| - ", t)

        # Clean
        cleaned = []
        for p in parts:
            p = p.strip(" -\t")
            if p:
                cleaned.append(p)
        return cleaned

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

        # Rule-based extraction using FULL chunk text
        extractions = []
        for r in results:
            full_text = (r.get("text") or "").strip()
            if not full_text:
                continue

            for stmt in self._split_statements(full_text):
                if OBLIGATION_PATTERN.search(stmt):
                    extractions.append({
                        "category": guess_category(stmt),
                        "obligation": stmt,
                        "doc_id": r["doc_id"],
                        "chunk_id": r["chunk_id"],
                        "source_file": r["source_file"],
                    })

        # If evidence match is weak, refuse (but still return what we found for transparency)
        if not evidence_ok:
            return {
                "ok": False,
                "reason": "Insufficient evidence for a supported extraction (weak semantic match).",
                "top_score": top_score,
                "margin": margin,
                "extractions": extractions,
                "results": results,
            }

        # Evidence match is OK, but no obligations detected
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
