import re
from typing import Dict, Any
from openai import OpenAI

from regdoc_agent.agents.lookup import LookupAgent
from regdoc_agent.agents.extract import ExtractAgent


class Orchestrator:
    """
    Routes user queries to the appropriate agent based on intent.
    """

    def __init__(self, client: OpenAI):
        self.lookup_agent = LookupAgent(client)

        # Extraction queries are broader, so thresholds are less strict.
        self.extract_agent = ExtractAgent(
            client,
            top_k=5,
            min_top_score=0.30,
            min_margin=0.05,
        )

    def classify_intent(self, query: str) -> str:
        """
        Very simple deterministic intent classifier.
        """
        q = query.lower()

        # Definition / explanation queries
        if re.search(r"\b(what is|define|explain)\b", q):
            return "lookup"

        # Extraction-style queries
        if re.search(r"\b(list|extract|show|identify)\b", q):
            return "extract"

        # Default fallback
        return "lookup"

    def run(self, query: str) -> Dict[str, Any]:
        intent = self.classify_intent(query)

        if intent == "lookup":
            out = self.lookup_agent.run(query)
            out["intent"] = "lookup"
            return out

        if intent == "extract":
            out = self.extract_agent.run(query)
            out["intent"] = "extract"
            return out

        # Fallback (shouldn't happen, but safe)
        return {
            "ok": False,
            "intent": "unknown",
            "reason": "Unable to classify query intent.",
            "results": [],
        }
