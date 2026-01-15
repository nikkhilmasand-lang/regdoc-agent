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
