"""
Challenge 3 - Multi-Turn Workflow Optimization Challenge
Token estimation method (from the challenge): estimated tokens = total characters / 4
Run: python Challenge3.py
"""

# ---- Stated assumptions (characters) ---------------------------------------
REPO_CHARS = 2_000_000          # whole ecommerce repository
ORIGINAL_REQUEST_CHARS = 400    # the one-shot "refactor everything" request
CONTRACT_CHARS = 1_100          # PROJECT_CONTRACT v1, referenced per stage
HANDOFF_CHARS = 1_500           # filled handoff template per stage
STAGE_INSTRUCTION_CHARS = 800   # stage-specific objective + gate text
STAGE_FILES_CHARS = 40_000      # average in-scope files per stage

STAGES = [
    {"id": 1, "name": "Discovery & Plan",                    "depends_on": [],        "dedicated_gate": False},
    {"id": 2, "name": "Data & API Contracts",                "depends_on": [1],       "dedicated_gate": False},
    {"id": 3, "name": "Authentication",                      "depends_on": [2],       "dedicated_gate": True},
    {"id": 4, "name": "Catalog, Search & Filters",           "depends_on": [2],       "dedicated_gate": False},
    {"id": 5, "name": "Checkout",                            "depends_on": [3, 4],    "dedicated_gate": False},
    {"id": 6, "name": "Payments",                            "depends_on": [5],       "dedicated_gate": True},
    {"id": 7, "name": "Interface, Accessibility & Perf",     "depends_on": [3, 4, 5, 6], "dedicated_gate": False},
    {"id": 8, "name": "Regression, Bug Closure & Release",   "depends_on": [1, 2, 3, 4, 5, 6, 7], "dedicated_gate": False},
]

WIDTH = 64


def tokens(chars: int) -> int:
    """Competition method: characters / 4 (rounded)."""
    return round(chars / 4)


def one_shot() -> int:
    return REPO_CHARS + ORIGINAL_REQUEST_CHARS


def per_stage_load() -> int:
    return CONTRACT_CHARS + HANDOFF_CHARS + STAGE_INSTRUCTION_CHARS + STAGE_FILES_CHARS


def naive_multi_turn() -> int:
    """Resend the full accumulated history at every stage: 1+2+...+N stage-loads."""
    n = len(STAGES)
    return per_stage_load() * (n * (n + 1) // 2)


def staged_with_handoff() -> int:
    return per_stage_load() * len(STAGES)


def validate_plan() -> list[tuple[str, bool]]:
    ids = {s["id"] for s in STAGES}
    by_id = {s["id"]: s for s in STAGES}
    checks = [
        ("6-8 stages", 6 <= len(STAGES) <= 8),
        ("Authentication has a dedicated gate",
         any(s["dedicated_gate"] and "auth" in s["name"].lower() for s in STAGES)),
        ("Payments has a dedicated gate",
         any(s["dedicated_gate"] and "payment" in s["name"].lower() for s in STAGES)),
        ("Every dependency points to an earlier stage",
         all(d in ids and d < s["id"] for s in STAGES for d in s["depends_on"])),
        ("Checkout depends on Authentication",
         3 in by_id[5]["depends_on"]),
        ("Payments depends on Checkout",
         5 in by_id[6]["depends_on"]),
        ("Release depends on all earlier stages",
         set(by_id[8]["depends_on"]) == ids - {8}),
        ("Contract referenced once per stage (not repeated history)",
         CONTRACT_CHARS < per_stage_load() * 0.1),
    ]
    return checks


def pct(a: int, b: int) -> float:
    return (a - b) / a * 100


def main() -> None:
    a, b, c = one_shot(), naive_multi_turn(), staged_with_handoff()

    print("=" * WIDTH)
    print("CHALLENGE 3 - MULTI-TURN WORKFLOW  (tokens = characters / 4)")
    print("=" * WIDTH)
    print(f"  {'Approach':<36}{'Chars':>14}{'Tokens':>12}")
    print("-" * WIDTH)
    print(f"  {'A. One-shot (whole repo)':<36}{a:>14,}{tokens(a):>12,}")
    print(f"  {'B. Naive multi-turn (full history)':<36}{b:>14,}{tokens(b):>12,}")
    print(f"  {'C. Staged + contract + handoff':<36}{c:>14,}{tokens(c):>12,}")
    print("-" * WIDTH)
    print(f"  Per-stage load (C)           : {tokens(per_stage_load()):>8,} tokens")
    print(f"  Contract (referenced, once)  : {tokens(CONTRACT_CHARS):>8,} tokens")
    print(f"  Reduction C vs A             : {pct(tokens(a), tokens(c)):>7.1f}%")
    print(f"  Reduction C vs B             : {pct(tokens(b), tokens(c)):>7.1f}%")

    print("\nSTAGE PLAN")
    print("-" * WIDTH)
    for s in STAGES:
        deps = ", ".join(map(str, s["depends_on"])) or "-"
        flag = "  [DEDICATED GATE]" if s["dedicated_gate"] else ""
        print(f"  {s['id']}. {s['name']:<38} deps: {deps}{flag}")

    print("\nCOMPETITION-RULE CHECK")
    print("-" * WIDTH)
    checks = validate_plan()
    for name, ok in checks:
        print(f"  [{'OK' if ok else 'FAIL':5}] {name}")
    passed = sum(ok for _, ok in checks)
    print("-" * WIDTH)
    print(f"  Rules satisfied: {passed}/{len(checks)}"
          f"  -> {'ALL RULES MET' if passed == len(checks) else 'REVIEW NEEDED'}")


if __name__ == "__main__":
    main()
