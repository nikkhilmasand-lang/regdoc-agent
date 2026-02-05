# RegDoc Agent

RegDoc Agent is a citation-first system for querying regulated or rule-heavy documents using semantic retrieval and tightly constrained reasoning.

The project is built around a simple idea: in regulated environments, **correctness, traceability, and knowing when to refuse** matter more than fluent or complete answers.

---

## What this is

RegDoc Agent is a public prototype that allows users to query regulatory-style documents and receive:

- Answers grounded strictly in retrieved source text  
- Explicit source references for every response  
- Structured outputs such as definitions or extracted obligations  
- Clear refusal when a question cannot be supported by available evidence  

The system is intentionally designed to favor **precision over coverage**.

---

## What this is not

- Not legal or compliance advice  
- Not connected to proprietary or internal company documents  
- Not a decision-making or approval system  
- Not a general-purpose chatbot  
- Not trained on user queries or private data  

All documents used are public or sanitized examples.

---

## Architecture (v1)

The system follows an agent-orchestrated retrieval flow.

![Architecture Diagram](docs/architecture_v1.png)

### High-level flow

1. A user submits a natural-language query  
2. An orchestrator classifies the query intent  
3. A task-specific agent is selected (lookup or extract)  
4. Relevant document chunks are retrieved via semantic search  
5. Evidence quality is evaluated using score and margin thresholds  
6. The system either:
   - returns a sourced answer, or  
   - explicitly refuses if evidence is insufficient  

Refusal is treated as a **correct and intentional outcome**.

---

## Core components

- **Orchestrator**  
  Routes queries based on intent (lookup vs. extract)

- **Lookup Agent**  
  Handles definition and explanation-style queries

- **Extract Agent**  
  Performs rule-based extraction of obligation-like statements using explicit language patterns (e.g., *must*, *shall*, *required*)

- **Retrieval Layer**  
  FAISS-based semantic search over embedded document chunks with traceable metadata

- **Guardrails & Refusal Logic**  
  Enforces evidence thresholds and prevents unsupported or misleading responses

- **Evaluation Harness**  
  Measures retrieval precision and validates expected refusals

---

## Scope and boundaries

This project deliberately limits scope to remain defensible and explainable.

- [Regulated Documents — Scope Definition](Notes/regulated_documents_scope.md)  
- [MVP Scope — Will Do / Will Not Do](Notes/mvp_scope.md)  
- [Design Decisions](docs/design_decisions.md)

---

## MVP scope (January)

**Included**
- Document ingestion and chunking  
- Vector-based semantic retrieval  
- Source-traceable results  
- Intent routing (lookup / extract)  
- Refusal-first behavior with explicit reasons  
- Retrieval evaluation and failure analysis  

**Excluded (v1)**
- UI or frontend work  
- Role-based access control  
- Production-grade security  
- Legal or compliance recommendations  
- Model fine-tuning  

---

## Current status

This repository represents an early but complete **v0.1 system**.

At this stage:
- Ingestion, semantic retrieval, and traceability are implemented  
- The system can extract obligation-style statements when evidence exists  
- Unsupported or out-of-scope queries are explicitly refused  
- Retrieval behavior is evaluated using a small test set  

The system prioritizes **safe behavior over answer completeness**.

---

## Quickstart (local demo)

### 1. Ingest documents
```bash
python scripts/ingest.py
2. Build semantic index
python scripts/build_index.py

3. Run queries
python scripts/query.py

Example queries
What is data privacy?

List all obligations mentioned in the documents

What is GDPR Article 6?

###License

MIT (public prototype)