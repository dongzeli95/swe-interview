# ML System Design — Cheat Sheet

The industry has converged on Alireza Dirafzoon's 9-step template (see `resources.md` #2). Every ML sys design round wants to see this scaffold. Adapt the emphasis per prompt, but keep the structure.

## Alireza's 9-Step Formula

1. **Problem statement & clarifying questions.** What's the business goal? What's the ML task type (classification / ranking / generation)? What are the constraints (latency, cost, privacy)?
2. **Data.** Where does it come from? Labels — implicit or explicit? Volume? Freshness? Sampling? Class imbalance?
3. **Model.** Start with a baseline (heuristic, logistic regression). Iterate to candidates. Justify the chosen model with trade-offs.
4. **Evaluation.** Offline: what metric? (precision/recall/F1, NDCG, AUC, calibration, BLEU/ROUGE, human eval for GenAI.) Online: A/B test setup, guardrail metrics.
5. **Deployment & Serving.** Batch vs real-time. Model server (Triton, TorchServe, vLLM). Latency budget. Autoscaling.
6. **Monitoring & feedback.** Distribution drift, data drift, concept drift. Model performance metrics. Prediction confidence. Alerting.
7. **Iteration.** Retraining cadence. Feature engineering next steps. A/B test → ship criteria.
8. **Considerations.** Fairness, bias, privacy (differential privacy, on-device), cost, energy.
9. **Deep dives / follow-ups.** Anticipate 1–2 places the interviewer will drill: model architecture, sharding, cold start, evaluations.

## Canonical prompts (drill these)

### Prompt 1: Design a recommendation system (feed ranking)

- Task: rank N candidate items for user U to maximize `p(engagement | user, item)`.
- Data: user activity log, item metadata, negative sampling from impressions-without-clicks.
- Model: two-tower (user tower + item tower) → dot product OR full DLRM.
- Serving: precompute user embeddings, ANN-index item embeddings, retrieve top-K, then re-rank with a heavier model.
- Deep dive candidates: cold start (new user, new item), fresh candidate injection, position bias.

### Prompt 2: Design a search ranker

- Task: given query Q and doc corpus D, return top-K docs.
- Two-stage: retrieval (BM25 + dense embedding, hybrid) → re-ranking (cross-encoder).
- Metrics: NDCG@10, MRR. Online: click-through rate, dwell time.
- Deep dive: query understanding, personalization, LTR (learning to rank).

### Prompt 3: Ad click-through prediction (CTR)

- Task: `p(click | user, ad, context)`.
- Feature engineering: hashing trick, cross-features.
- Model: logistic regression baseline → factorization machines → DeepFM / DCN.
- Calibration matters more than raw AUC (revenue = CTR × bid).
- Deep dive: online learning, feature store, sharding.

### Prompt 4: Fraud detection pipeline

- Task: binary classification on transactions.
- Extreme class imbalance (fraud ~0.1%). Discuss sampling, focal loss, cost-sensitive learning.
- Real-time serving (<50ms). Feature pipeline: streaming (Flink / Kafka Streams).
- Metrics: precision at fixed recall, PR-AUC (NOT ROC-AUC).
- Deep dive: adversarial adaptation (fraudsters evolve), model retraining cadence.

### Prompt 5: RAG system for a doc corpus

- Task: answer user questions grounded in corpus.
- Pipeline: doc ingestion → chunking → embedding → vector store → retrieval → LLM → post-processing.
- Chunking strategy: fixed-size vs semantic vs hierarchical.
- Retrieval: dense (embedding) vs hybrid (BM25 + dense).
- Reranking: cross-encoder for top-100 → top-10.
- Evals: retrieval hit rate, faithfulness, answer relevance, groundedness (RAGAS).
- Deep dive: hallucination detection, source citation, multi-hop questions.

### Prompt 6: Evals pipeline for an LLM product

- Task: build an offline + online evaluation harness for an LLM-backed product.
- Offline: golden test set (100–1000 curated examples), LLM-as-judge (with disclaimers), rubric-based scoring, regression on prior wins.
- Online: user satisfaction (thumbs up/down), completion rate, follow-up rate.
- CI: every model change → auto-run eval → block ship if regressions.
- Deep dive: eval-set drift, cost of evals, human-in-the-loop for gold labels.

## GenAI-flavored twists (frontier lab loops)

Frontier labs (OpenAI, Anthropic, DeepMind) often modify sys design prompts:

- "Design a serving stack for a 400B-parameter model at 500K QPS." — leads into vLLM, paged attention, KV-cache management, batch scheduling, multi-tenancy.
- "Design an RLHF training pipeline for a chat model." — leads into reward model training, PPO vs DPO, preference dataset generation, safety-vs-helpfulness.
- "Design a way to evaluate whether a model is being jailbroken." — leads into red-team dataset, classifier training, human review pipeline.
- "Design a fine-tuning-as-a-service API." — leads into LoRA/QLoRA, job scheduling, base-model versioning, cost model.

## Common failure modes in these rounds

- **Diving into architecture first.** Interviewer wants #1 (problem clarification) for a full 5 minutes. Slow down.
- **Skipping metrics.** Naming an accuracy number without acknowledging the underlying distribution and cost matrix.
- **No mention of monitoring.** Every design must include drift detection + retraining trigger.
- **Overengineering serving.** Junior candidates ML sys design like they're building Google. State the volume assumption and match it.
- **Not proposing a baseline.** Even for GenAI, propose "heuristic → simple model → fine-tuned LLM" progression.
