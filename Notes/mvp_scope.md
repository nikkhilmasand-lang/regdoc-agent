# MVP Scope — Will Do / Will Not Do (v1)

## Will do (v1)

- Ingest public or sanitized regulatory documents
- Chunk documents and attach metadata (source, section, date)
- Perform vector-based semantic retrieval
- Generate answers strictly from retrieved text
- Include citations for all key claims
- Use a simple agent router to delegate tasks

---

## Will not do (v1)

- Fancy or production UI
- Role-based access control (RBAC)
- Production-grade security hardening
- Live external system integrations
- Legal or compliance advice
- Automated decision-making or approvals

---

## Rationale

The MVP is intentionally constrained to:
- Reduce surface area for errors
- Make system behavior easier to reason about
- Enable honest evaluation of failure modes

Additional complexity will only be introduced once correctness and traceability are well understood.
