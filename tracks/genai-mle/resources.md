# GenAI MLE — Reading List

Sourced from the 1point3acres thread [*25找AI ML engineer 用的材料分享*](https://www.1point3acres.com/bbs/thread-1127325-1-1.html) (thread-1127325, jasonYue and contributors, May 2025 – Feb 2026 with ongoing updates), plus canonical additions.

Local PDF export of the thread: `/Users/benli/Downloads/25找AI ML engineer 用的材料分享_一亩三分地求职（非面经）版.pdf`.

## Core reference — the foundation

### 1. Karpathy — Neural Networks: Zero to Hero

- **Repo:** https://github.com/karpathy/nn-zero-to-hero
- **Format:** ~10 YouTube lectures with companion Jupyter notebooks. Free.
- **Why:** builds intuition from micrograd → makemore → tokenizer → GPT-2 from scratch. Not skippable — MLE interviewers will ask you to explain attention or backprop and you need to have implemented both.
- **Contributor quote (thread):** *"Karpathy 从 zero to hero"* — used to secure an intern return offer.

### 2. Alireza Dirafzoon — Machine Learning Interviews (ML System Design)

- **Repo:** https://github.com/alirezadir/Machine-Learning-Interviews
- **Key file:** `src/MLSD/ml-systemdesign.md` — the **9-step ML system design formula** the whole industry has converged on:
  1. Problem statement, requirements, and clarifying questions
  2. Data (source, features, labels)
  3. Model (baseline → candidates → chosen)
  4. Evaluation (offline + online metrics)
  5. Deployment & serving
  6. Monitoring & feedback loop
  7. Iteration
  8. Considerations (fairness, privacy, cost)
  9. Deep dives / follow-ups
- **Why:** the ByteByteGo-endorsed structure. Master this template — every ML sys design round wants to see it.

### 3. Chip Huyen — Designing Machine Learning Systems + AI Engineering

- **Book 1:** *Designing Machine Learning Systems* (O'Reilly, 2022). Applied MLE bible.
- **Book 2:** *AI Engineering* (O'Reilly, 2024). GenAI-specific — RAG, fine-tuning, evals, prompt engineering.
- **Site / free resources:** https://huyenchip.com/ — blog posts on RLHF, fine-tuning, MLOps.
- **Why:** *AI Engineering* is the closest thing to a canonical text for the specific GenAI MLE role.

## LLMs — hands-on

### 4. Hands-On Large Language Models (O'Reilly)

- **Repo:** https://github.com/HandsOnLLM/Hands-On-Large-Language-Models (8.5k+ stars)
- **Authors:** Jay Alammar, Maarten Grootendorst.
- **Why:** working notebooks for embeddings, semantic search, prompt engineering, RAG, fine-tuning. Complements Karpathy's from-scratch approach.

### 5. Sebastian Raschka — LLMs from Scratch

- **Repo:** https://github.com/rasbt/LLMs-from-scratch
- **Book:** *Build a Large Language Model (From Scratch)* (Manning, 2024).
- **Why:** more polished sibling to Karpathy's zero-to-hero. Structured book with runnable code for every chapter.

### 6. HuggingFace LLM Course

- **URL:** https://huggingface.co/learn/llm-course (formerly the NLP course, updated to LLMs).
- **Why:** free, hands-on with transformers library, PEFT, TRL. The de facto industry API.

## ML interview questions (targeted)

### 7. andrewekhalel/MLQuestions

- **Repo:** https://github.com/andrewekhalel/MLQuestions
- **Focus:** classical ML + CV interview Q&A. Good for filling gaps if your ML fundamentals are rusty.

### 8. Educatum — GenAI / LLM interview question banks

- **Site:** https://www.educatum.com/llm-and-genai-advanced-interview-questions
- **AI/ML Pathway Study Group:** structured cohort — Part I Fundamentals, Week 2 Core Concepts (Regression/Classification/Optimization). Uses Stanford ML-005 (Andrew Ng) as lecture backbone.

### 9. Hoang — Top 50 LLM Interview Questions

- **PDF:** https://bit.ly/50-llm-interview-questions

### 10. LLM & GenAI Interview Questions (community list)

- **URL:** https://bit.ly/llm-and-genai-interview-questions

### 11. Top AI Labs Interview Questions (OpenAI, Anthropic, DeepMind)

- **URL:** https://bit.ly/openAI-interview
- **Sample topics visible in the thread:**
  - Versioned Key-Value Store Design (System Design)
  - Design a Scalable Webhook System
  - Refactor a Chat Service for Bots (OOD)
  - Frontend System Design for a Conversation
  - Implement a Resumable Iterator
  - Implement a Multiple ResumableFileIterator
  - Implement Spreadsheet API

## University lecture series

### 12. Stanford CS 329S — Machine Learning Systems Design

- **URL:** https://stanford-cs329s.github.io/
- **Instructor:** Chip Huyen (same author as book #3).
- **Why:** the course that seeded the industry standard. Lecture notes + reading list are the practical minimum.

### 13. fast.ai — Practical Deep Learning for Coders

- **URL:** https://course.fast.ai/
- **Why:** top-down, code-first. Best for engineers pivoting who don't want to sit through six weeks of linear regression.

### 14. Stanford ML-005 (Andrew Ng) — for classical ML fundamentals

- Used inside the Educatum pathway (see #8) for Week 2 core concepts (Logistic Regression Lecture 6, etc.). Skip if you already have solid ML fundamentals.

## Engineering blogs — the "400 engineering blogs" reference in the thread

The thread cites a curated set of ~400 AI/ML engineering blog posts. Rather than list them all, prioritize:

- OpenAI research blog + cookbook
- Anthropic engineering blog
- Meta AI blog
- Google Research + DeepMind blog
- HuggingFace blog (very hands-on)
- LangChain blog (RAG patterns, evals)
- Sebastian Raschka's Ahead of AI newsletter
- Simon Willison — https://simonwillison.net/ — practical LLM engineering
- Lilian Weng — https://lilianweng.github.io/ — deep technical dives (was at OpenAI)

## Additional canonical resources (not in thread, worth adding)

- **Attention Is All You Need** — original transformer paper. Read after Karpathy.
- **The Illustrated Transformer** — https://jalammar.github.io/illustrated-transformer/
- **Let's Build GPT** (Karpathy YouTube) — 2h video, standalone.
- **DeepLearning.AI short courses** — https://learn.deeplearning.ai/ — 1–2h focused courses on RAG, function calling, evals, agents.
- **LangChain / LlamaIndex documentation** — pick one and build a RAG app end-to-end.
- **Full Stack LLM Bootcamp** — https://fullstackdeeplearning.com/llm-bootcamp/ — free, production-focused.

## How to use this list

Do NOT try to read everything. Prioritize:

1. **Weeks 1–3:** Karpathy zero-to-hero (#1) + fast.ai (#13) if you're new.
2. **Weeks 4–6:** Chip Huyen books (#3) + Alireza's ML sys design template (#2).
3. **Weeks 7–9:** Hands-On LLMs (#4) + build one project end-to-end (RAG chatbot with evals).
4. **Weeks 10–12:** Interview question banks (#7, #8, #9, #11) as drilling material.

Update this list as the 1point3acres thread gets new picks. Re-export the PDF to the same path and diff.
