# Token Optimization Challenges — Fresher AI Competition

Practical, reproducible solutions to three **Token Optimization** challenges for AI coding assistants (Claude, Kiro, or any AI tool). Each challenge tackles a different way that teams waste tokens — and quality — when working with AI, and shows how to fix it without losing requirements, safety, or verification.

| Challenge | Theme | Level | One-line idea |
|-----------|-------|-------|---------------|
| [1 — Prompt Compression](./challenge-1-prompt-compression/) | Write less, say everything | Beginner | Turn a rambling prompt into a structured one and cut ~58% of tokens with zero lost requirements |
| [2 — Context Selection](./challenge-2-context-selection/) | Send only what matters | Beginner–Intermediate | Debug a 401 after an auth upgrade using ~0.4% of the repository's tokens |
| [3 — Multi-Turn Workflow](./challenge-3-multi-turn-workflow/) | Split big work into verified stages | Intermediate | Replace a "refactor everything" one-shot with 8 gated stages, a shared contract, and compact handoffs |

---

## Why this repository exists

Large prompts and oversized context are the most common reason AI coding tools become slow, expensive, and unreliable. The three challenges here cover the full lifecycle of that problem:

1. **The prompt itself** is too long and repetitive → *Challenge 1*
2. **The attached context** is the whole repository instead of the failure path → *Challenge 2*
3. **The task** is too big for one turn and ships unverified changes → *Challenge 3*

Every solution follows the same principles:

- **Preserve every requirement and safety condition** — shorter never means vaguer.
- **Make the result understandable without the original material.**
- **Explain both the token savings and how quality was preserved.**
- **Make the numbers reproducible** with a small, dependency-free Python script.

---

## Token estimation method

All three challenges use the competition's comparison method:

```text
estimated tokens = total characters ÷ 4
```

This is intentionally simple. Real billing tokens vary by model, language, punctuation, and tokenizer — the method is for *comparing* approaches, not for invoicing.

---

## Challenge summaries

### Challenge 1 — Prompt Compression

**Problem:** A product team's prompt asking an AI assistant to add CSV export to a React analytics dashboard is long, conversational, and repeats itself three times.

**Solution:** A structured `Task / Rules / Steps` prompt that keeps all 12 requirements (filtered + sorted rows, visible column order, hidden columns excluded, ISO 8601 dates, no new dependency, inspect-then-implement-then-report, no regression).

| | Original | Optimized |
|---|---|---|
| Characters | 879 | 368 |
| Estimated tokens | ≈ 220 | ≈ 92 |
| Reduction | | **≈ 58%** |

**Deliverables:** optimized prompt · original and optimized token counts · percentage reduction · five-line explanation of what was removed and preserved.

➡ [Read the full submission](Challenge1.md)

### Challenge 2 — Context Selection

**Problem:** A TypeScript web app returns **HTTP 401 from `GET /api/profile`** after an authentication package upgrade. Login works; the protected request fails. The repo has hundreds of unrelated files — what do you send to the AI?

**Solution:** Follow the failing request **browser → cookie → middleware → route** and send only that path plus what changed: the exact 401 and server error lines, auth middleware, the `/api/profile` route, the client request (credential options), sanitized session/cookie config, auth package versions, the auth-only upgrade diff, repro steps, and runtime environment. Everything else — 250 components, 80 routes, lockfile, generated clients, unrelated tables, six months of build logs, images — is excluded. Secrets are masked before anything is sent.

| | All available material | Selected context + prompt |
|---|---|---|
| Estimated tokens | ~941,000 | ~3,550 |
| Reduction | | **≈ 99.6%** |

**Deliverables:** included-context checklist · excluded-context checklist · final debugging prompt · reasoning for the selection · estimated token comparison.

➡ [Read the full submission](Challenge2.md)

### Challenge 3 — Multi-Turn Workflow Optimization

**Problem:** A company asks an AI tool to refactor an entire ecommerce platform in one prompt — auth, database, catalog, search, checkout, payments, accessibility, tests, performance, bugs, and deployment — "end to end without stopping".

**Solution:** An 8-stage workflow ordered by dependency and risk, each stage with a defined input, output, and **measurable gate**. Authentication and Payments get **dedicated verification gates**, and later stages cannot start until their prerequisites pass. A single reusable **project contract** holds stable coding, security, and completion rules, and a compact **handoff template** carries only decisions, gate evidence, and in-scope files — never the full conversation.

```text
[1 Discovery] -> [2 Contracts] -> [3 Auth] ------\
                        \                        -> [5 Checkout] -> [6 Payments] -> [7 UI/A11y/Perf] -> [8 Release]
                         -> [4 Catalog] ---------/
```

| Approach | Estimated tokens |
|----------|-----------------:|
| One-shot (whole repo) | ~500,000 |
| Naive multi-turn (resend full history) | ~390,000 |
| **Staged + contract + handoff** | **~87,000 (≈ 83% less than one-shot)** |

**Deliverables:** staged workflow · input/output/gate per stage · reusable context contract outline · context handoff template · token-saving and quality explanation.

➡ [Read the full submission](Challenge3.md)

---

## Running the scripts

Each challenge folder contains a small Python script that reproduces the token numbers and runs automated checks (requirement preservation, competition rules, dependency ordering). They use only the standard library.

```bash
# Requirements: Python 3.9+
git clone (https://github.com/AaronSam-30052003/AI-Token-Optimization-Arena.git)
python challenge1.py
python challenge2.py
python challenge3.py
```

Each script prints a submission-style report; 

---

## Notes and assumptions

- Character counts for Challenge 1 are exact for the given text; counts for Challenges 2 and 3 use **stated size assumptions** because the challenge documents list categories, not file sizes. Each folder's README documents those assumptions so they can be swapped for real numbers.
- Line endings affect character counts by ±1–2; files are saved with LF endings for reproducibility.
- Nothing in this repository requires API keys or paid services.

## License

MIT — feel free to reuse the prompts, contract, and handoff template in your own projects.
