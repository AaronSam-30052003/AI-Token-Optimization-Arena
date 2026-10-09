"""
Challenge 2 - Context Selection Challenge
Token estimation method (from the challenge): estimated tokens = total characters / 4
Run: python challenge2.py
"""

INCLUDED = {
    "Exact 401 response + 2 server error lines": 600,
    "Authentication middleware":                 3_000,
    "Protected /api/profile route":              1_500,
    "Client profile request":                    1_200,
    "Session and cookie config (sanitized)":     1_500,
    "Authentication package versions":           400,
    "Auth-related upgrade diff":                 4_000,
    "Reproduction steps":                        400,
    "Runtime environment details":               600,
}

EXCLUDED = {
    "250 unrelated React components (~3,000 each)": 250 * 3_000,
    "80 unrelated API routes (~2,000 each)":        80 * 2_000,
    "Complete package lockfile":                    600_000,
    "Generated API client files":                   200_000,
    "Unrelated database tables":                    40_000,
    "Six months of successful build logs":          2_000_000,
    "UI snapshots, icons, images (binary)":         0,
}

DEBUG_PROMPT = """Task: Diagnose why GET /api/profile returns HTTP 401 after upgrading the auth package (<pkg> <old> -> <new>). Login succeeds; the protected request fails.

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
3. Verification steps for: login, session persistence across refresh, and GET /api/profile returning 200."""

# Competition rules the prompt must satisfy
RULES = {
    "Exact error kept (401 / /api/profile)":       ["401", "/api/profile"],
    "Reproduction path kept":                      ["repro", "sign in"],
    "Client side covered":                         ["client"],
    "Server side covered":                         ["middleware", "route"],
    "Secrets masked":                              ["masked"],
    "Evidence-based hypotheses requested":         ["hypotheses", "evidence"],
    "Smallest safe fix, no blind rewrite":         ["smallest safe fix", "no rewrites"],
    "Verification: login/session/protected route": ["verification", "login", "session", "/api/profile"],
}

WIDTH = 66


def tokens(chars: int) -> int:
    """Competition method: characters / 4 (rounded)."""
    return round(chars / 4)


def section(title: str, items: dict[str, int]) -> int:
    print("\n" + title)
    print("-" * WIDTH)
    total = 0
    for name, chars in items.items():
        total += chars
        print(f"  {name:<48}{chars:>10,}{tokens(chars):>8,}")
    print("-" * WIDTH)
    print(f"  {'TOTAL':<48}{total:>10,}{tokens(total):>8,}")
    return total


def main() -> None:
    print("=" * WIDTH)
    print("CHALLENGE 2 - CONTEXT SELECTION  (tokens = characters / 4)")
    print("=" * WIDTH)
    print(f"  {'Category':<48}{'Chars':>10}{'Tokens':>8}")

    inc = section("INCLUDED CONTEXT", INCLUDED)
    prompt_chars = len(DEBUG_PROMPT)
    print(f"  {'+ Debugging prompt itself':<48}{prompt_chars:>10,}{tokens(prompt_chars):>8,}")
    inc_total = inc + prompt_chars

    exc = section("EXCLUDED CONTEXT", EXCLUDED)
    everything = inc + exc

    reduction = (tokens(everything) - tokens(inc_total)) / tokens(everything) * 100
    print("\nTOKEN COMPARISON")
    print("-" * WIDTH)
    print(f"  All available material : {tokens(everything):>10,} tokens")
    print(f"  Selected + prompt      : {tokens(inc_total):>10,} tokens")
    print(f"  Reduction              : {reduction:>9.1f}%")

    print("\nCOMPETITION-RULE CHECK ON THE PROMPT")
    print("-" * WIDTH)
    lower = DEBUG_PROMPT.lower()
    passed = 0
    for rule, keys in RULES.items():
        ok = all(k in lower for k in keys)
        passed += ok
        print(f"  [{'OK' if ok else 'MISSING':7}] {rule}")
    print("-" * WIDTH)
    print(f"  Rules satisfied: {passed}/{len(RULES)}"
          f"  -> {'ALL RULES MET' if passed == len(RULES) else 'REVIEW NEEDED'}")


if __name__ == "__main__":
    main()
