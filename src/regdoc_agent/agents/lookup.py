"""
LookupAgent

Purpose:
Handles definition-style and explanatory queries over regulated documents.

Examples:
- "What is data privacy?"
- "What does risk management involve?"
- "Define reporting standards"

Responsibilities:
- Receive a user query
- Call the retrieval layer to fetch relevant document chunks
- Return retrieved passages with source metadata
- Do NOT generate new information
- Do NOT answer if evidence is insufficient

Notes:
This agent does not perform reasoning or summarization yet.
It is a thin wrapper over retrieval, added to make system behavior explicit.
"""
from typing import List, Dict
from openai import OpenAI

from regdoc_agent.retrieval.semantic import retrieve_chunks


class LookupAgent:
    """
    Handles definition-style and explanatory queries by returning retrieved evidence.
    """

    def __init__(self, client: OpenAI):
        self.client = client

    def run(self, query: str) -> List[Dict]:
        return retrieve_chunks(client=self.client, query=query, top_k=5)
