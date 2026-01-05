# RegDoc Agent

Agentic, citation-first question answering over regulated documents using retrieval and constrained generation.

This project focuses on **correctness, traceability, and controlled behavior** when interacting with rule-heavy documents such as regulations, standards, and compliance guidance.

---

## What this is

RegDoc Agent is a prototype system that allows users to query regulated documents and receive:

- Answers grounded strictly in retrieved source text
- Explicit citations for every key claim
- Structured outputs (definitions, obligations, timelines, comparisons)
- Clear refusal when answers cannot be supported by sources

The system is intentionally designed to favor **precision over coverage**.

---

## What this is not

- Not legal or compliance advice
- Not connected to proprietary or internal company documents
- Not a decision-making or approval system
- Not a general-purpose chatbot
- Not trained on user queries

---

## Architecture (v1)

The system uses an agent-orchestrated retrieval flow.

![Architecture Diagram](docs/architecture_v1.png)

**High-level flow:**

1. User submits a natural-language query
2. Orchestrator classifies the request type
3. A specialized agent handles the task
4. Relevant document sections are retrieved via semantic search
5. The agent produces an answer **only from retrieved evidence**
6. Output is returned with citations

---

## Core components

- **Orchestrator Agent**  
  Routes queries to the appropriate task agent based on intent

- **Task Agents**
  - Lookup Agent (definitions / requirements)
  - Compare Agent (document or section comparison)
  - Extract Agent (obligations, timelines, exceptions)

- **Retrieval Layer**  
  Semantic search over embedded document chunks with metadata filtering

- **Document Store & Ingestion**  
  Public or sanitized regulatory documents indexed with metadata

- **Guardrails & Formatter**  
  Enforces citation requirements and prevents unsupported responses

---

## Scope & boundaries

The project deliberately limits scope to ensure safe, defensible behavior.

- [Regulated Documents — Scope Definition](Notes/regulated_documents_scope.md)
- [MVP Scope — Will Do / Will Not Do](Notes/mvp_scope.md)

---

## MVP scope (January)

**Included**
- Document ingestion
- Vector-based retrieval
- Source-cited answers
- Simple agent routing

**Excluded (for v1)**
- Fancy UI
- Role-based access control
- Production-grade security
- Legal or compliance recommendations

---

## Repo status

This repository represents an **early-stage but evolving system**.

Planned progression:
- **v1:** Skeleton, retrieval, citations
- **v2:** Evaluation, failure modes, refusals
- **v3:** Polish, documentation, reuse

---

## Roadmap

- [x] Scope definition
- [x] Architecture v1
- [ ] Ingestion pipeline
- [ ] Retrieval + citations
- [ ] Agent routing
- [ ] Evaluation harness

---

## License

MIT (public prototype)
