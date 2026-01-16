from typing import List, Dict, Any
from openai import OpenAI

from regdoc_agent.retrieval.semantic import retrieve_chunks


class LookupAgent:
    """
    Handles definition-style and explanatory queries by returning retrieved evidence.
    Adds refusal behavior when evidence is weak or non-specific.
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
                "results": results,
            }

        top_score = results[0]["score"]
        second_score = results[1]["score"] if len(results) > 1 else None
        margin = (top_score - second_score) if second_score is not None else None

        ok_by_score = top_score >= self.min_top_score
        ok_by_margin = (margin is None) or (margin >= self.min_margin)

        ok = ok_by_score and ok_by_margin

        if not ok:
            reason_bits = []
            if not ok_by_score:
                reason_bits.append(f"top_score below threshold ({top_score:.3f} < {self.min_top_score:.2f})")
            if margin is not None and not ok_by_margin:
                reason_bits.append(f"evidence not specific enough (margin {margin:.3f} < {self.min_margin:.2f})")

            return {
                "ok": False,
                "reason": "Insufficient evidence for a supported answer: " + "; ".join(reason_bits) + ".",
                "top_score": top_score,
                "margin": margin,
                "results": results,
            }

        return {
            "ok": True,
            "top_score": top_score,
            "margin": margin,
            "results": results,
        }
