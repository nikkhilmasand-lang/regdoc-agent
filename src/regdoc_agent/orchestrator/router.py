import re
from typing import Dict, Any
from openai import OpenAI

from regdoc_agent.agents.lookup import LookupAgent


class Orchestrator:
    """
    Routes user queries to the appropriate agent based on intent.
    """

    def __init__(self, client: OpenAI):
        self.lookup_agent = LookupAgent(client)

    def classify_intent(self, query: str) -> str:
        """
        Very simple deterministic intent classifier.
        """
        q = query.lower()

        # Definition / explanation queries
        if re.search(r"\b(what is|define|explain)\b", q):
            return "lookup"

        # Extraction-style queries (stub for now)
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

        # Extract agent will be implemented later
        return {
            "ok": False,
            "intent": "extract",
            "reason": "Extract agent not implemented yet.",
            "results": [],
        }
