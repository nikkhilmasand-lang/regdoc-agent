# Regulated Documents — Scope Definition

## What “regulated documents” means

In this project, *regulated documents* refers to documents that are governed by formal rules or oversight, not documents that are confidential or private by default.

These documents typically:
- Are published or released by regulatory bodies, standards organizations, or institutions
- Contain precise definitions, obligations, exceptions, and timelines
- Require careful interpretation, where small wording changes can materially alter meaning
- Demand accuracy and traceability when queried

Examples include publicly available regulations, guidance notes, compliance frameworks, policy standards, and other rule-driven documents that people routinely struggle to navigate correctly.

The primary challenge with these documents is **interpretive risk**, not access.
A partially correct or hallucinated answer can be more harmful than no answer.

---

## What is intentionally excluded

This project does **not** include:
- Internal company policies or manuals
- Proprietary compliance documentation
- Client-specific materials
- Confidential filings or correspondence
- Any documents obtained through employment or non-public access

If examples resemble internal policies, they are either fully sanitized or purpose-built mock documents created solely to demonstrate structure and behavior.

No real organizational data is used.

---

## Why this boundary exists

The goal of this project is to study **how AI systems should behave around regulated information**, not to demonstrate access to sensitive data.

By limiting the corpus to public and sanitized documents, the system can be built, tested, and discussed openly while still addressing the harder problem:

> How to deliver answers that are grounded, constrained, and traceable in rule-heavy environments.

This boundary keeps the focus on system design — routing, retrieval, guardrails, and citation — rather than data acquisition.

---

## Summary

This project works with documents that are *regulated by nature*, not documents that are *confidential by access*, in order to study correctness, traceability, and control in AI-assisted information retrieval.
