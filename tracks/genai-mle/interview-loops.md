# GenAI MLE — Interview Loops By Company

Based on public reports (1point3acres, Blind, Glassdoor) and the 1point3acres thread `resources.md` references. Structures change — treat as directional, not authoritative.

## Frontier labs

### OpenAI
- Recruiter screen → HM screen → ~5 onsite rounds.
- Rounds reported (from the thread's "Top AI Companies Interview Questions" list):
  - System design (versioned KV store, scalable webhook system)
  - OOD (chat service for bots, spreadsheet API)
  - Frontend system design (design a conversation UI)
  - Coding (implement a resumable iterator, multiple resumable file iterator)
- ML content depth varies by team — Applied vs Research vs API.
- Bar: production seriousness + willingness to reason about safety.

### Anthropic
- Recruiter → 1–2 phone screens (coding + values) → onsite (~5 rounds).
- Rounds: coding (LC + one applied), ML sys design, ML depth, research discussion, values.
- Values round is real, not fluff. Read their Acceptable Use Policy and Responsible Scaling Policy before applying.
- Very heavy on `why Anthropic` and `how do you think about safety`.

### DeepMind (Google)
- Longer loop (6+ rounds sometimes).
- Rounds: 2 coding, 1 ML depth, 1 ML sys design, 1 research/paper discussion, 1 googlyness/leadership.
- Publication history matters more here than at OpenAI/Anthropic.

### Meta AI / GenAI
- FAANG-standard loop (5 rounds) but ML sys design replaces one coding round.
- Rounds: 2 coding, 1 ML sys design, 1 ML depth (including transformer internals), 1 behavioral.
- Products: LLaMA, Meta AI assistant, ranking models.

### xAI
- Small, opinionated loops. Often starts with a "build something" project take-home.
- Very Elon-loop-ish: sharp technical bar, less HR polish.

## GenAI product companies

### Perplexity
- 4 rounds typically: coding, ML/GenAI depth, RAG-specific sys design, cultural.
- Very interested in your take on hallucination, citations, and evals.

### Fireworks AI (referenced in thread — Lin Qiao's company)
- Serving-heavy focus. Expect deep dives on inference optimization, vLLM, batching, LoRA serving.
- Systems bar high — this is closer to platform infra than product ML.

### Cursor / Sourcegraph / Replit
- Code-oriented AI companies. Coding rounds tend to lean toward real-world tooling problems.
- Sourcegraph publishes tons of engineering content — read before interviewing.

### Cohere
- Standard 5-round loop but with a very strong "why LLMs" narrative check.
- Model quality + safety focus.

### Together AI, Mistral (US team), Databricks Mosaic
- Infra-heavy. Distributed training experience is a discriminator.

## Big-tech GenAI teams

### Uber AI FDE (Field Data Engineer / Applied)
- More production ML than research. LC + ML sys design + case study.

### Airbnb GenAI, Instacart AI
- Applied ML flavor. Recommendation, ranking, generation for product.
- Coding stays LC-standard. ML sys design is the differentiator.

### LinkedIn Generative AI
- Ranking + LLM-augmented product. ML sys design with heavy focus on evals and A/B.

### Google Apprentice / L3
- Standard Google loop, ML content added.

## What to prepare per round type

| Round | Prep source in this repo |
|---|---|
| Coding (LC-style) | `algorithm/` + [`../swe-senior-staff/problems.md`](../swe-senior-staff/problems.md) |
| ML coding (implement X) | [`./ml-coding.md`](./ml-coding.md) |
| ML sys design | [`./ml-sys-design.md`](./ml-sys-design.md) |
| System design (generic) | `system-design/` |
| OOD | `ood/` |
| Behavioral | `behavioral/` + `Amazon Principal Leadership Prep.txt` |
| Research discussion | Read 3 recent papers from target company. Anthropic: transformer circuits. OpenAI: GPT-4 tech report, o1 blog. |
| Cultural / values | Read the company's public writing (blog, values page) end-to-end before onsite. |

## General advice

- Loops for GenAI roles are longer than SWE loops. Budget 4–6 weeks per company from first contact to onsite.
- Compensation ranges are wider — do not undersell yourself; base + equity structures vary drastically.
- Referrals compound: one contact at a lab is worth ten cold applications.
- Publicly available signal (github, blog, side project) matters more here than for SWE roles. If you can, ship a GenAI project before applying.
