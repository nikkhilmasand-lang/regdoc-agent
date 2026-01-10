# RegDoc Agent

RegDoc Agent is a citation-first system for querying regulated or rule-heavy documents using semantic retrieval and tightly constrained generation.

The project is built around a simple idea: in regulated environments, **correctness, traceability, and refusal** matter more than fluent answers.

---

## What this is

RegDoc Agent is a public prototype that allows users to query regulatory-style documents and receive:

- Answers grounded strictly in retrieved source text  
- Explicit source references for every response  
- Structured outputs such as definitions, obligations, timelines, or comparisons  
- Clear refusal when a question cannot be supported by available evidence  

The system is intentionally designed to favor **precision over coverage**.

---

## What this is not

- Not legal or compliance advice  
- Not connected to proprietary or internal company documents  
- Not a decision-making or approval system  
- Not a general-purpose chatbot  
- Not trained on user queries or private data  

All documents used are public or sanitized.

---

## Architecture (v1)

The system follows an agent-orchestrated retrieval flow.

![Architecture Diagram](docs/architecture_v1.png)

### High-level flow

1. A user submits a natural-language query  
2. An orchestrator classifies the query type  
3. A task-specific agent is selected  
4. Relevant document sections are retrieved via semantic search  
5. Responses are produced strictly from retrieved evidence  
6. Output is returned with clear source references  

---

## Core components

- **Orchestrator**  
  Routes queries based on intent (lookup, extract, compare)

- **Task agents**  
  - Lookup agent (definitions, requirements)  
  - Compare agent (sections or documents)  
  - Extract agent (obligations, timelines, exceptions)

- **Retrieval layer**  
  Semantic search over embedded document chunks with metadata

- **Document ingestion**  
  Public or sanitized regulatory documents, chunked and indexed with traceability

- **Guardrails & formatting**  
  Enforces citation requirements and prevents unsupported responses

---

## Scope and boundaries

This project deliberately limits scope to remain defensible and explainable.

- [Regulated Documents — Scope Definition](Notes/regulated_documents_scope.md)  
- [MVP Scope — Will Do / Will Not Do](Notes/mvp_scope.md)

---

## MVP scope (January)

**Included**
- Document ingestion and chunking  
- Vector-based semantic retrieval  
- Source-traceable results  
- Minimal routing logic  

**Excluded (v1)**
- UI or frontend work  
- Role-based access control  
- Production-grade security  
- Legal or compliance recommendations  

---

## Current status

This repository represents an early but working system.

At this stage:
- Ingestion, semantic retrieval, and source traceability are implemented  
- The system can retrieve and rank relevant document passages for a query  
- Agent routing and evaluation will be layered next  

---

## Quickstart (local demo)

### 1. Ingest documents
python scripts/ingest.py
### 2. Build semantic index
python scripts/build_index.py

### 3. Query the system
python scripts/query.py


### Example query:

What is data privacy?


The system retrieves the most relevant document passages with clear source references.

Example queries

What is data privacy?

Why is reporting important in organizations?

What does risk management involve?

### Roadmap

 Scope definition

 Architecture v1

 Ingestion pipeline

 Semantic retrieval with traceability

 Agent routing

 Evaluation and failure analysis

### License

MIT (public prototype)