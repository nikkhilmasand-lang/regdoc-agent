# Design Decisions

This document explains the key design choices behind RegDoc Agent and why they were made.  
The goal of the project is not to maximize feature count, but to build a system that behaves predictably and defensibly when working with regulated or rule-heavy documents.

---

## Why citation-first answers

In regulated environments, an answer is only as good as the evidence supporting it.

Instead of generating free-form responses, the system is designed to:
- Retrieve relevant source text first
- Produce answers only when there is explicit supporting evidence
- Always surface where an answer came from

This reduces ambiguity and makes it clear to a user (or reviewer) what the system actually knows versus what it does not.

---

## Why refusal is a first-class outcome

One of the most important design choices was treating refusal as a **correct outcome**, not a failure.

In early experiments, it became clear that answering every question creates more risk than value.  
If a question cannot be supported by the available documents, the safest behavior is to say so explicitly.

The system therefore refuses to answer when:
- Semantic similarity to the document corpus is weak
- Retrieved evidence is ambiguous or conflicting
- A query asks about content that is outside the indexed documents

This mirrors how real compliance or risk systems behave in practice.

---

## Why semantic retrieval is separated from generation

Retrieval and answer logic are intentionally decoupled.

The system first focuses on **finding relevant evidence**, and only then decides whether an answer can be produced. This separation makes it easier to:
- Evaluate retrieval quality independently
- Add safeguards before any generation step
- Explain why an answer was or was not returned

It also allows future changes to generation logic without changing how evidence is sourced.

---

## Why FAISS and vector similarity

FAISS was chosen as a simple, well-understood baseline for semantic search.

The goal at this stage is not advanced ranking, but:
- Deterministic behavior
- Transparent scoring
- Easy inspection of retrieved results

Using normalized embeddings with cosine similarity allows the system to reason about relevance in a consistent way, while still exposing scores and margins that can be used for refusal thresholds.

---

## Why rule-based extraction (for now)

For extraction-style queries (e.g., obligations), the system currently uses lightweight, rule-based detection rather than full language-model generation.

This is intentional.

Regulated documents often use specific language (“must”, “shall”, “required”), which can be identified reliably without introducing hallucination risk. Starting with rules:
- Keeps behavior explainable
- Avoids inventing obligations that do not exist
- Makes failures easier to debug

LLM-assisted extraction can be layered later once safeguards are clearly defined.

---

## Why evaluation was added early

Instead of relying on anecdotal testing, a small evaluation harness was added early in the project.

This allows the system to be tested against:
- Questions that should succeed
- Questions that should refuse
- Edge cases that test retrieval precision

Measuring behavior makes it possible to reason about improvements and prevents silent regressions as the system evolves.

---

## Scope discipline

Many features were intentionally deferred:
- No UI
- No role-based access
- No legal recommendations
- No training on user queries

These omissions are deliberate. The focus is on correctness, traceability, and controlled behavior, not on production readiness or user experience.

---

## Summary

Every design decision in this project is guided by a single principle:

> It is better to return no answer than a misleading one.

RegDoc Agent is meant to be a careful, evidence-driven system that demonstrates how AI tools can behave responsibly in regulated contexts.
