# swe-interview

Personal fork of https://github.com/dongzeli95/swe-interview restructured for a **three-track** interview prep:

1. [**SWE Senior/Staff**](./tracks/swe-senior-staff/) — FAANG-tier senior/staff SWE loops.
2. [**Quant Trading**](./tracks/quant/) — Citadel, Two Sigma, Jump Trading, HRT, Jane Street.
3. [**GenAI MLE**](./tracks/genai-mle/) — pivot into GenAI Machine Learning Engineer roles at OpenAI, Anthropic, DeepMind, and applied ML teams.

## Layout

```
swe-interview/
├── algorithm/                # Shared DSA drills (used by all tracks)
│   └── <category>/
│       ├── python/           # Python solutions  (primary)
│       ├── cpp/              # C++ solutions     (reference)
│       ├── md/               # Problem writeups
│       └── README.md
├── system-design/            # Shared: DDIA notes, deep-dives, mocks
├── behavioral/               # Shared
├── ood/                      # Shared object-oriented design
├── company-tags/             # Per-company mock question sets
└── tracks/
    ├── README.md
    ├── swe-senior-staff/     # Track-specific roadmap, problem index
    ├── quant/                # Probability, C++ fundamentals, systems, resources
    └── genai-mle/            # ML coding, ML sys design, reading list, loops
```

**Python is primary.** All 148 C++ solutions have matching Python ports at `algorithm/<category>/python/*.py` — same underlying algorithm, same number of solution approaches. C++ files remain as reference.

## Where to start

- Reading the [`tracks/README.md`](./tracks/README.md) first.
- Then the specific track's `README.md` → `roadmap.md` → `problems.md` / `resources.md`.

## From the upstream repo

Upstream also has a GitBook: https://dongzeli95s-organization.gitbook.io/swe-interview-handbook/ — good for quick reference on the underlying problem set. The SUMMARY.md still drives that book; it was updated to reflect the new folder layout.
