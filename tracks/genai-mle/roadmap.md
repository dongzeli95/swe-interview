# GenAI MLE — 12 Week Roadmap

The pivot from SWE → GenAI MLE takes longer than the other tracks because the domain fluency is genuinely broader. Assumes 10–15 hrs/week.

## Weeks 1–3: Foundations

**Goal:** be able to explain (a) how a transformer works, (b) how backprop works on it, (c) what tokenization is, without hand-waving.

- Karpathy's *Neural Networks: Zero to Hero* (see [`resources.md`](./resources.md) #1). Do all 10 lectures with the notebooks. Build makemore → mini-GPT.
- If your ML fundamentals are thin: fast.ai lecture 1–4 (`resources.md` #13) in parallel.
- End of week 3 checkpoint: implement scaled dot-product attention from scratch in a fresh file, no reference. Explain masking and multi-head.

## Weeks 4–5: ML fundamentals refresh

**Goal:** answer classical ML questions without googling — L1/L2, bias/variance, regularization, cross-entropy, softmax numerics, batch norm.

- MLQuestions repo (`resources.md` #7). Work through 60% of it. Skip CV-heavy sections if not applicable.
- Read Chip Huyen *Designing Machine Learning Systems* Ch. 1–5 (`resources.md` #3).
- Stanford ML-005 (Andrew Ng) for topics where you have gaps.

## Weeks 6–7: LLM engineering

**Goal:** be able to design and build a RAG app with evals.

- Hands-On LLMs (`resources.md` #4) — work through the notebooks: embeddings, semantic search, prompt engineering, RAG, fine-tuning.
- Chip Huyen *AI Engineering* (`resources.md` #3, book 2) — Ch. 1–7.
- HuggingFace LLM course (`resources.md` #6) — transformers + PEFT + TRL sections.
- **Project:** build one end-to-end RAG app (documents → chunker → embedder → vector store → retriever → LLM → evals). Use LangChain or LlamaIndex. Ship it.

## Weeks 8–9: ML System Design

**Goal:** own Alireza's 9-step template. Practice on 6 canonical designs.

- Alireza's ML System Design (`resources.md` #2). Memorize the 9-step formula.
- [`ml-sys-design.md`](./ml-sys-design.md) — work each of the 6 canonical prompts:
  1. Design a recommendation system (feed ranking)
  2. Design a search ranker
  3. Design an ad click-through prediction system
  4. Design a fraud detection pipeline
  5. Design a RAG system for a doc corpus
  6. Design an evals pipeline for an LLM product
- Do 2 ML sys design mocks with a peer or on interviewing.io.

## Week 10: ML coding + LC in Python

**Goal:** the "implement X from scratch" round.

- [`ml-coding.md`](./ml-coding.md) — 15 problems. Implement each from scratch:
  - k-means, KNN, linear regression via normal eqs and via GD
  - Attention (scaled dot-product, multi-head)
  - Softmax with numerical stability
  - Cross-entropy loss with backward pass
  - Tokenizer (BPE step-by-step)
  - PCA via SVD
  - Naive Bayes classifier
  - LSTM cell forward pass
  - Beam search decoder
  - Top-k / nucleus sampling
- Keep drilling LC in Python (see the SWE track's `problems.md`).

## Week 11: Company-specific loop research

- Read [`interview-loops.md`](./interview-loops.md). Note company-specific round types.
- Target companies: OpenAI, Anthropic, DeepMind, Meta (GenAI), Perplexity, Fireworks AI, Cursor, Cohere.
- Study interview report sites (1point3acres, Blind, Glassdoor) for the last 6 months.
- Prepare 4 hero stories tuned to GenAI: "hardest ML/data bug", "biggest evals surprise", "product decision from evals", "shipped something despite ambiguity".

## Week 12: Full-loop simulation

- 1 ML sys design + 1 ML coding + 1 LC + 1 behavioral in a single day.
- Post-mortem; retire.

## Ongoing

- 1 GenAI/LLM interview question per day from `resources.md` #8/#9/#11.
- Read 1 paper per week from the [Anthropic reading list](https://transformer-circuits.pub/) or Lilian Weng's blog.
- Follow HuggingFace's `TheBloke`, Together AI, Fireworks AI for model release notes — you're expected to know what's out.
