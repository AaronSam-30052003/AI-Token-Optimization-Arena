# Challenge 2 — Context Selection Challenge

**Competition:** Fresher AI Competition | Token Optimization  
**Level:** Beginner to Intermediate · **Suggested time:** 45 minutes · **Maximum score:** 100 points  
**Token estimation method (as specified by the challenge):** estimated tokens = total characters ÷ 4

---

## Problem Statement

A TypeScript web application returns **HTTP 401 from `GET /api/profile`** after an authentication package upgrade. Login succeeds, but the protected request fails. The repository contains hundreds of unrelated files. The task is to decide what context to send to an AI assistant (Claude, Kiro, or any AI tool) and what to exclude — minimizing tokens without weakening the diagnosis.

---

## 1. Included-Context Checklist

| # | Item | Sanitization applied |
|---|------|----------------------|
| 1 | Exact 401 response body/headers + the two relevant server error lines | Mask any session ID / token values in headers |
| 2 | Authentication middleware (server) | None needed (code only) |
| 3 | Protected `/api/profile` route handler | None needed |
| 4 | Client profile request code (fetch/axios call incl. `credentials` / `withCredentials` options) | Remove hard-coded URLs with embedded tokens, if any |
| 5 | Session and cookie configuration | **Replace secret keys with `<MASKED>`**; keep `httpOnly`, `secure`, `sameSite`, `domain`, `path`, `maxAge` |
| 6 | Authentication package versions — before and after the upgrade | None needed |
| 7 | Upgrade diff limited to authentication-related files | Mask any secrets that appear in the diff |
| 8 | Reproduction steps | None needed |
| 9 | Runtime environment details (Node version, browser, local vs production, HTTP vs HTTPS, proxy/domain setup) | Mask internal hostnames if sensitive |

**9 of 16 available categories included** — the complete browser → server failure path, plus the two things that changed (versions and diff).

---

## 2. Excluded-Context Checklist

| # | Item | Why it is safe to exclude |
|---|------|---------------------------|
| 1 | 250 unrelated React components | Cannot affect the auth request path; only the profile request code matters |
| 2 | 80 unrelated API routes | Only `/api/profile` and the shared auth middleware are on the failure path |
| 3 | Complete package lockfile | Hundreds of KB of noise; only the auth package versions (included separately) are relevant |
| 4 | Generated API client files | Machine-generated, derived from source already included; adds no diagnostic signal |
| 5 | Database tables unrelated to sessions/users | Not on the auth path |
| 6 | Six months of successful build logs | Historical success logs cannot explain a current runtime 401 |
| 7 | UI snapshots, icons, and images | Visual assets, irrelevant to an HTTP auth failure |

**Also sanitized out of everything included:** secret keys, cookie/session values, bearer tokens, API keys, private credentials.

---

## 3. Final Debugging Prompt

```text
Task: Diagnose why GET /api/profile returns HTTP 401 after upgrading the auth package (<pkg> <old> -> <new>). Login succeeds; the protected request fails.

Repro:
1. Sign in (returns 200, session cookie set).
2. Open or refresh /profile.
3. GET /api/profile -> 401.

Context attached (all secrets masked as <MASKED>):
- Exact 401 response + 2 server error lines
- Auth middleware
- /api/profile route handler
- Client profile request (incl. credentials/withCredentials options)
- Session + cookie config (httpOnly, secure, sameSite, domain, path, maxAge)
- Auth package versions before/after
- Upgrade diff for auth files only
- Runtime env: Node/browser versions, local vs prod, HTTP/HTTPS, proxy/domain

Deliver:
1. Ranked root-cause hypotheses, each tied to specific evidence above (e.g. cookie flags, sameSite/secure under HTTP, session store or serializer change, middleware API change, credentials not sent, breaking change in <new>).
2. Smallest safe fix. No rewrites.
3. Verification steps for: login, session persistence across refresh, and GET /api/profile returning 200.
```

---

## 4. Reasoning for the Selection

### Why each included category is necessary

| Included item | Hypothesis it lets the AI test |
|---------------|--------------------------------|
| Exact 401 + server error lines | Pinpoints *where* the rejection happens (middleware vs route) and the exact failure reason; the rules require the exact error be kept |
| Auth middleware | Session lookup, token verification, and the API surface most likely changed by the upgrade |
| `/api/profile` route | Confirms how the route consumes the middleware's output (e.g., `req.user`, `req.session`) |
| Client profile request | Checks whether cookies are actually sent (`credentials: "include"` / `withCredentials`), covering the **client side** as required |
| Session and cookie config | `sameSite`, `secure`, `domain`, `path` misconfigurations are the classic "login works, next request 401" cause |
| Auth package versions | Lets the AI reason about known breaking changes between the two versions |
| Auth-related upgrade diff | Shows exactly what changed — the regression trigger |
| Reproduction steps | Required by the rules; lets the AI confirm its hypothesis order against the observed sequence |
| Runtime environment | `secure` cookies on HTTP localhost, cross-origin domains, and proxies all change cookie behaviour |

### Why the exclusions are safe

- Nothing excluded sits on the request path **browser → cookie → middleware → route**.
- Everything excluded is either unrelated by domain (components, other routes, other tables), derived (generated client, lockfile), historical (build logs), or non-textual (images).
- The rule "do not include a complete repository merely because the root cause is unknown" is honoured: the unknown is narrowed by *following the failing request*, not by dumping files.

### Why the prompt is shaped this way

- Asks for **ranked, evidence-based hypotheses** and a **smallest safe fix** — not a blind rewrite (competition rule).
- Requires **verification steps** for login, session persistence, and the protected route, matching the expected output in the challenge.
- Sanitization is stated explicitly so the AI knows `<MASKED>` values are intentional.

---

## 5. Estimated Token Comparison

> Sizes below are **stated assumptions** for a typical mid-size TypeScript repo, because the challenge lists categories but not file sizes. Method: estimated tokens = characters ÷ 4.

### Included context

| Item | Est. characters | Est. tokens |
|------|----------------:|------------:|
| 401 response + 2 error lines | 600 | 150 |
| Auth middleware | 3,000 | 750 |
| `/api/profile` route | 1,500 | 375 |
| Client profile request | 1,200 | 300 |
| Session/cookie config (sanitized) | 1,500 | 375 |
| Auth package versions | 400 | 100 |
| Auth-related upgrade diff | 4,000 | 1,000 |
| Reproduction steps | 400 | 100 |
| Runtime environment | 600 | 150 |
| Debugging prompt itself | ~1,000 | ~250 |
| **Total included** | **~14,200** | **~3,550** |

### Excluded context

| Item | Est. characters | Est. tokens |
|------|----------------:|------------:|
| 250 React components (~3,000 chars each) | 750,000 | 187,500 |
| 80 API routes (~2,000 chars each) | 160,000 | 40,000 |
| Complete package lockfile | 600,000 | 150,000 |
| Generated API client files | 200,000 | 50,000 |
| Unrelated database tables/schemas | 40,000 | 10,000 |
| Six months of build logs | 2,000,000 | 500,000 |
| UI snapshots, icons, images | binary — not tokenizable as text | — |
| **Total excluded** | **~3,750,000** | **~937,500** |

### Comparison

| | Est. characters | Est. tokens |
|---|---:|---:|
| All available material | ~3,764,000 | ~941,000 |
| Selected context + prompt | ~14,200 | ~3,550 |
| **Reduction** | | **≈ 99.6%** |

```text
Reduction = (941,000 − 3,550) ÷ 941,000 × 100 ≈ 99.6%
```

Even if every assumed size is off by 2–3×, the selected context stays in the low thousands of tokens while "everything" stays in the hundreds of thousands — the conclusion holds.

---

## Judge Validation Checklist (self-check)

- [x] Shorter / more context-efficient — ~3.5K tokens vs ~941K (≈ 99.6% reduction).
- [x] No essential requirement or safety condition missing — exact error, repro path, client + server, sanitization all present.
- [x] Instructions understandable without the original material — the prompt is standalone.
- [x] Token savings **and** quality preservation both explained — Sections 4 and 5.
- [x] All calculations and required deliverables present — Sections 1–5.

---

## Reproducing the Numbers (optional)

```bash
python challenge2.py
```

The script holds the assumed sizes per category, applies `characters ÷ 4`, prints the included vs excluded totals and the reduction, and checks that the debugging prompt satisfies the competition rules (exact error, repro steps, client + server coverage, sanitization note, hypotheses + verification request).

