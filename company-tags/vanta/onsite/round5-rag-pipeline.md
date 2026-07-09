# Round 5 — AI Technical Deep-Dive: RAG for Compliance Docs

Newer onsite round. Reported prompt: **Design an AI/RAG pipeline related to Vanta's GRC product.**

## Context

Vanta automates compliance (SOC 2, ISO 27001, HIPAA, GDPR, PCI, etc.). Their AI-facing product surface:
- Ingest customer's internal docs (security policies, employee handbooks, vendor agreements, cloud config exports).
- Analyze them for compliance gaps against a target framework.
- Suggest remediation, generate evidence for auditors, answer compliance-vocabulary questions.

**They do NOT expect you to know GRC.** They expect you to know RAG architecture cold, and to reason about the compliance domain from first principles when they steer the discussion.

## Skeleton (reuse Alireza's 9-step + RAG specifics)

Cross-reference: [`../../../tracks/genai-mle/ml-sys-design.md`](../../../tracks/genai-mle/ml-sys-design.md).

### 1. Problem statement

- Customer uploads a corpus of internal docs.
- System answers questions grounded in those docs OR flags compliance gaps against a framework (e.g., "does this cover access review?").
- Bar: answers must cite sources (compliance is untrustworthy without citations); model must NOT hallucinate control coverage.

### 2. Data

- **Inputs:** PDFs, DOCX, HTML pages exported from Confluence/Notion/Google Docs, CSV of asset inventories, JSON from cloud audit exports (AWS Config, GCP Cloud Asset Inventory).
- **Framework knowledge:** SOC 2 Trust Services Criteria, ISO 27001 Annex A, etc. — a curated corpus Vanta maintains internally.
- **Labels for evals:** hand-curated question/answer pairs from Vanta's own SMEs.

### 3. Model / architecture

```
┌────────────┐   ┌───────────┐   ┌──────────────┐   ┌────────────────┐
│  Ingestion │──▶│ Chunker   │──▶│ Embedder     │──▶│ Vector store   │
│  (PDF/HTML │   │           │   │ (bge, e5,    │   │ (pgvector /    │
│  parsers)  │   │           │   │  OpenAI text │   │  Weaviate /    │
└────────────┘   └───────────┘   │  -embed-3)   │   │  Pinecone)     │
                                 └──────────────┘   └────────────────┘
                                                             │
                                                             ▼
┌────────────┐   ┌──────────────┐   ┌─────────────┐   ┌────────────┐
│ User query │──▶│ Query reform │──▶│ Retriever   │──▶│ Reranker   │
│            │   │ (LLM-based,  │   │ (hybrid:    │   │ (cross-    │
│            │   │  optional)   │   │  BM25 +     │   │  encoder)  │
└────────────┘   └──────────────┘   │  vector)    │   └────────────┘
                                    └─────────────┘         │
                                                            ▼
                                          ┌───────────────────────────┐
                                          │  LLM (Claude / GPT-4-turbo)│
                                          │  + system prompt          │
                                          │  + retrieved chunks       │
                                          │  + citation guardrail     │
                                          └───────────────────────────┘
                                                            │
                                                            ▼
                                          ┌────────────────────────────┐
                                          │  Post-processor: citations,│
                                          │  fact-check pass,          │
                                          │  no-answer fallback        │
                                          └────────────────────────────┘
```

### Chunking strategy (they WILL ask)

- Naive fixed-size (500 tokens) chunking loses structure. Compliance docs have headings, tables, control IDs — chunking should respect them.
- Recommended: hierarchical chunking + parent-doc retrieval. Small chunks for retrieval, larger parent context in the LLM prompt.
- Table extraction: PDFs of policies often have tables (control matrices). Use a layout-aware parser (Unstructured.io, Azure Doc Intelligence, LlamaParse).

### Retrieval

- **Hybrid** (BM25 + dense embeddings) beats dense-only for compliance because control names / IDs are keyword-heavy.
- Metadata filters — every chunk tagged with `doc_id`, `section`, `framework`, `control_id`, `last_updated`. Filter before ANN search.
- Reranking: cross-encoder on top-50 → top-10.

### Generation

- Model choice: Claude 3.5 Sonnet or GPT-4-turbo for reasoning; smaller models for orchestration.
- System prompt enforces: "Cite source doc + section number for every claim. If the corpus doesn't cover the question, say 'This is not addressed in your uploaded policies.'"
- Constrained output for gap analysis: force JSON with `{control_id, is_covered, evidence: [chunk_ids], remediation}`.

### 4. Evaluation (spend real time here)

Compliance context makes evals load-bearing:

- **Retrieval quality:** hit rate @ K, MRR against a golden set.
- **Faithfulness (RAGAS):** does the answer only use information in retrieved chunks?
- **Groundedness:** every claim has a citation.
- **Answer relevance:** does the answer address the question?
- **Coverage:** for gap analysis, precision/recall vs SME-labeled gaps.
- **Hallucination detection:** LLM-as-judge on a held-out set with disclaimers.
- **Regression suite:** every model change → run 200-example golden set, block ship on regression.

### 5. Serving

- API: streaming responses for the chat UI, non-streaming for the analysis job.
- Async gap-analysis job: batch all controls, run in parallel, return report.
- Caching: query-level (Redis, 24h TTL), embedding-level (persistent — embeddings are expensive).
- Rate limiting per customer.

### 6. Monitoring & feedback

- Log every query + retrieved chunks + answer + citations.
- User feedback: 👍/👎, "the answer was wrong because..." (freeform).
- Drift detection: shift in retrieval distributions after new doc upload.
- Cost per query, tail latency (p95, p99).

### 7. Iteration

- V1: single-framework (SOC 2 only), off-the-shelf embedder, GPT-4-turbo.
- V2: multi-framework, hybrid retrieval, custom reranker.
- V3: agentic flow — LLM decides when to search vs when to answer, when to escalate to a human.
- V4: fine-tuned embedding on compliance corpus for domain shift.

### 8. Considerations

- **Data isolation.** Every customer's data must stay in their tenant. Vector index is per-tenant; multi-tenant embedding models are OK as long as inference doesn't leak.
- **Privacy.** Customer data cannot be used to train foundation models. If using OpenAI/Anthropic APIs, use zero-retention endpoints and get contractual guarantees.
- **PII detection.** Compliance docs may contain PII (employee names in a policy). Redact before indexing or before sending to a third-party API.
- **Audit trail.** Every LLM interaction is logged (compliance meta-story). What did we retrieve? What did we generate? Immutable audit log.
- **Human-in-the-loop.** For high-stakes claims (SOC 2 control coverage), gate on human approval before customer-visible.

### 9. Deep dives the interviewer WILL steer to

- **Hallucination mitigation.** Answer:
  - Constrain output format (structured JSON, "no answer" is a valid response).
  - Post-hoc verifier LLM checks answer-vs-chunks consistency.
  - LLM-as-judge on a held-out set as a regression gate.
- **Doc changes / re-indexing.** Customer updates their access policy. What do you do?
  - Incremental re-index on `last_updated` changes.
  - Version chunks; keep old + new so audit history is preserved.
- **Multi-doc reasoning.** "Are our access reviews compliant?" spans employee handbook + IAM audit log + AWS Config export. Needs multi-hop retrieval OR an agent.
- **Cold start.** New customer with zero docs. What does the product show them?
  - Framework-default recommendations, ask for specific doc uploads.
- **Cost.** Embed once (cheap-ish), rerank per query (moderate), LLM generate per query (expensive). Cost model:
  - Ingest: 100 docs × 500 chunks × $0.0001 = $5/customer one-time.
  - Query: $0.02–$0.10 per query depending on top-k and LLM tier.

## What you must not skip

- **Citations.** Every claim → source. Vanta sells to auditors; no citation, no product.
- **Evals.** If you don't mention offline+online evals in the first 10 min, you're behind.
- **Multi-tenancy.** Say the word.

## Prep reading

- `tracks/genai-mle/ml-sys-design.md` in this repo — the 9-step scaffold generalized.
- `tracks/genai-mle/resources.md` — Alireza's repo, Chip Huyen's AI Engineering (RAG chapter).
- RAGAS docs (https://docs.ragas.io/) — the vocabulary of RAG evals.
- Vanta's own blog (https://www.vanta.com/resources/) — read their AI product announcements before the round.
