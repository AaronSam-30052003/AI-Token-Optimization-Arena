# Challenge 3 — Multi-Turn Workflow Optimization Challenge

**Competition:** Fresher AI Competition | Token Optimization  
**Level:** Intermediate · **Suggested time:** 60 minutes · **Maximum score:** 100 points  
**Token estimation method (as specified by the challenge):** estimated tokens = total characters ÷ 4

---

## Problem Statement

A company asks an AI coding tool to refactor an entire ecommerce platform in a single prompt: modernize authentication, update the database, redesign the product catalog, improve search and filters, rebuild checkout, integrate payments, fix accessibility, write all tests, improve performance, solve all existing bugs, and deploy everything — "end to end without stopping".

A one-shot request of this size will overflow context, miss requirements, and ship unverified changes. This submission designs a token-efficient, verified multi-turn workflow.

---

## 1. Staged Workflow

Eight stages, ordered by **dependency** (what must exist first) and **risk** (what must be isolated and verified before anything depends on it).

| Stage | Name | Primary outcome | Depends on | Risk |
|-------|------|-----------------|-----------|------|
| 1 | Discovery & Plan | Approved scope, bug triage, ordered plan — no code | — | Low |
| 2 | Data & API Contracts | Schema migrations + API contracts | 1 | Medium |
| 3 | Authentication | Modernized auth flow | 2 | **High — dedicated gate** |
| 4 | Catalog, Search & Filters | Product management, search, filtering | 2 | Medium |
| 5 | Checkout | Cart → order flow (no payment capture yet) | 3, 4 | Medium |
| 6 | Payments | Test-mode payment integration + webhooks | 5 | **High — dedicated gate** |
| 7 | Interface, Accessibility & Performance | Integrated UI, a11y fixes, performance budget met | 3–6 | Medium |
| 8 | Regression, Bug Closure & Release | Full regression, residual bug fixes, deployment plan | 1–7 | High |

### Dependency flow

```text
[1 Discovery] -> [2 Contracts] -> [3 Auth] ------\
                        \                        -> [5 Checkout] -> [6 Payments] -> [7 UI/A11y/Perf] -> [8 Release]
                         -> [4 Catalog] ---------/
```

### How the original request maps to stages

| Original request item | Handled in |
|-----------------------|-----------|
| Modernize authentication | Stage 3 |
| Update the database | Stage 2 |
| Redesign product catalog | Stage 4 |
| Improve search and filters | Stage 4 |
| Rebuild checkout | Stage 5 |
| Integrate payments | Stage 6 |
| Fix accessibility | Stage 7 |
| Write all tests | Every stage gate requires tests for that stage's surface (not one giant test stage) |
| Improve performance | Stage 7 (budgets) + Stage 8 (regression) |
| Solve all existing bugs | Triaged in Stage 1, fixed in the owning stage, residual closed in Stage 8 |
| Deploy everything | Stage 8 |

---

## 2. Input / Output / Gate for Each Stage

### Stage 1 — Discovery & Plan
- **Input:** repository map (file tree + key modules), current error/bug list, product requirements, shared project contract.
- **Output:** architecture summary, risk register, dependency graph, bug triage (stage owner per bug), ordered plan. **No code changes.**
- **Gate:** scope, protected behaviors, and stage order approved by the human owner.

### Stage 2 — Data & API Contracts
- **Input:** approved plan, current schema files, existing API route signatures.
- **Output:** migration scripts (dev environment), typed API contracts (request/response types), rollback script.
- **Gate:** migrations apply and roll back cleanly on a dev database; type generation passes; schema validation passes.

### Stage 3 — Authentication *(dedicated verification gate)*
- **Input:** project contract, auth contracts from Stage 2, auth-related files only (middleware, session/cookie config, login/logout routes, client auth calls).
- **Output:** migrated authentication flow with tests.
- **Gate:** sign-in, sign-out, session refresh, protected-route access (200) and denial (401/403), password/secret handling review — all pass. **No later stage starts until this gate passes.**

### Stage 4 — Catalog, Search & Filters
- **Input:** catalog contracts from Stage 2, catalog/search files only.
- **Output:** product CRUD, search, filtering changes with tests.
- **Gate:** list, search, filter, sort, pagination, and CRUD checks pass; search latency within agreed budget.

### Stage 5 — Checkout
- **Input:** checkout contracts, auth decisions summary (Stage 3), catalog decisions summary (Stage 4), checkout files only.
- **Output:** cart → address → order creation flow (payment step stubbed), with tests.
- **Gate:** order created for authenticated user, cart totals correct (tax/shipping/discount), inventory reservation, guest/edge cases pass.

### Stage 6 — Payments *(dedicated verification gate)*
- **Input:** payment contracts, checkout decisions summary (Stage 5), payment files only, provider test-mode credentials as `<MASKED>` references.
- **Output:** test-mode payment integration with webhook handler and idempotency keys.
- **Gate:** success, decline, retry, cancellation, refund, webhook signature verification, idempotent replay, and no secret in code/logs — all pass. **Stage 7 does not start until this passes.**

### Stage 7 — Interface, Accessibility & Performance
- **Input:** completed feature surfaces (Stages 3–6) as component list + routes, design tokens, performance budgets.
- **Output:** integrated UI, accessibility corrections, performance optimizations.
- **Gate:** keyboard navigation, labels/ARIA, focus order, color contrast, responsive breakpoints pass; Core Web Vitals / bundle-size budgets met.

### Stage 8 — Regression, Bug Closure & Release
- **Input:** concise summaries + changed-file lists from Stages 2–7, residual bug list from Stage 1 triage, deployment target details.
- **Output:** full regression results, residual bug fixes, release checklist, staged deployment plan with rollback.
- **Gate:** all type, test, build, and security checks green; all Stage 1 protected behaviors verified; rollback rehearsed. **Only then publish.**

---

## 3. Reusable Project Instruction Contract (outline)

Stored once (e.g. `PROJECT_CONTRACT.md`) and **referenced by name** in every stage instead of being repeated.

```text
PROJECT CONTRACT v1 — ecommerce-refactor

Stack & patterns
- Use the existing stack, folder layout, and naming conventions. No new frameworks.
- Add a dependency only if justified in the stage output.

Security
- Validate all external input at the boundary.
- Never hard-code, log, or print secrets; reference env vars only.
- Preserve auth checks on every protected route.

Behavior preservation
- Do not change supported behavior outside the current stage's scope.
- Preserve existing accessibility (labels, keyboard, focus).

Quality gates (run before reporting)
- Type check, lint, unit + integration tests for touched areas, build.

Completion report format
- Changed files (path + one-line purpose)
- Decisions made and alternatives rejected
- Verification evidence (commands run + results)
- Open questions / unresolved decisions

Scope discipline
- One primary outcome per stage. Stop at the gate; do not continue into later stages.
```

Estimated size: ~1,100 characters → **~275 tokens**, sent once per stage by reference rather than re-explained.

---

## 4. Context Handoff Template

Used at the start of every stage. It carries **decisions and artifacts**, never the full conversation.

```text
STAGE <N> — <Stage name>
Contract: PROJECT_CONTRACT v1 applies (do not restate).

Objective (one outcome):
<single sentence>

Prior-stage summary (max 8 lines):
- Stage <N-1> gate: PASSED on <date> — evidence: <test suite / command + result>
- Key decisions carried forward: <decision 1>, <decision 2>
- Interfaces you must honor: <contract/type names>

Unresolved decisions for this stage:
- <question 1>
- <question 2>

Files/contracts in scope (only these):
- <path 1>
- <path 2>

Out of scope (do not touch):
- <areas owned by other stages>

Gate for this stage:
- <measurable check 1>
- <measurable check 2>

Deliver per contract report format.
```

Typical filled size: ~1,500 characters → **~375 tokens** per stage.

---

## 5. Token-Saving and Quality Explanation

### Token comparison (estimated, characters ÷ 4)

> Sizes are **stated assumptions** for a mid-size ecommerce codebase; the challenge gives the request but not repository sizes.

| Approach | What is sent | Est. characters | Est. tokens |
|----------|--------------|----------------:|------------:|
| **A. One-shot** (original request) | Whole repo (~2,000,000 chars) + 400-char request | ~2,000,400 | **~500,100** |
| **B. Naive multi-turn** (resend full history each stage) | Stage inputs accumulate: 1+2+…+8 = 36 stage-loads × 43,400 | ~1,562,400 | **~390,600** |
| **C. Staged with contract + handoff (this design)** | 8 × (contract 1,100 + handoff 1,500 + stage instructions 800 + stage files ~40,000) | ~347,200 | **~86,800** |

```text
Reduction vs one-shot        = (500,100 − 86,800) ÷ 500,100 × 100 ≈ 83%
Reduction vs naive multi-turn = (390,600 − 86,800) ÷ 390,600 × 100 ≈ 78%
```

Per stage, the design sends **~10,850 tokens** instead of the whole repository, and the contract (~275 tokens) is referenced rather than re-explained, saving roughly 7 × 275 ≈ 1,900 tokens of repetition alone across the workflow. Even if the repo is half or double the assumed size, the proportions hold because stage context is bounded by scope, not by repository size.

### Why token use drops

1. **Bounded context per turn** — each stage receives only its own files and contracts, not the repository.
2. **Contract by reference** — stable coding, security, and completion rules are stated once and cited, never repeated.
3. **Decisions, not transcripts** — the handoff carries an 8-line summary, gate evidence, and open questions; the full conversation is never resent.
4. **Fewer retries** — a failed gate is caught immediately in a small context, instead of surfacing after a 500K-token one-shot that must be redone.

### Why quality and safety improve

1. **High-risk work is isolated** — authentication (Stage 3) and payments (Stage 6) each have a dedicated gate with explicit security checks (session handling, protected routes, webhook signatures, idempotency, no secrets in code/logs).
2. **Dependencies are enforced** — later stages cannot start until their required gates pass, so checkout never builds on unverified auth, and payments never build on unverified checkout.
3. **One primary outcome per stage** — the AI cannot drift into other areas; scope discipline is in the contract.
4. **Measurable gates** — every stage ends with pass/fail checks, not "looks done".
5. **Protected behavior is approved up front** (Stage 1) and re-verified at release (Stage 8), catching regressions.
6. **Tests are written where the code is written** — each gate requires tests for that stage's surface, instead of a single "write all tests" step that would arrive too late to prevent dependent breakage.

---

## Judge Validation Checklist (self-check)

- [x] Shorter / more context-efficient — ~87K tokens vs ~500K one-shot (≈ 83% reduction).
- [x] No essential requirement or safety condition missing — all 11 request items mapped; auth and payments have dedicated gates; secrets handled via contract.
- [x] Instructions understandable without the original material — contract and handoff template are standalone.
- [x] Token savings **and** quality preservation both explained — Section 5.
- [x] All calculations and required deliverables present — Sections 1–5.

---

## Reproducing the Numbers (optional)

```bash
python Challenge3.py
```

The script models the three approaches with the stated assumptions, applies `characters ÷ 4`, prints the comparison, and validates the stage plan against the competition rules (dedicated auth/payment gates, dependency ordering, one outcome per stage).

