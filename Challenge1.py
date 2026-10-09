"""
Challenge 1 - Prompt Compression Challenge
Token estimation method (from the challenge): estimated tokens = total characters / 4
Run: python challenge1.py
"""

ORIGINAL_PROMPT = (
    "Hello, I need you to help me with something in our React dashboard. "
    "We have a table on the analytics page and users are asking for export. "
    "Please add an export button so they can export the table. The export should be CSV. "
    "Please remember that it must export whatever rows the user is currently seeing after "
    "applying filters, because filtered data is important. Sorting should also be respected. "
    "Keep the columns in the same visible order. Hidden columns must not be exported. "
    "Dates should be in ISO 8601 format. Please do not add another package or dependency. "
    "Before changing anything, inspect the project and tell me which files are relevant. "
    "Then implement it. After implementation, tell me what files changed and how to verify "
    "the feature. Please make sure existing filtering and sorting still work. "
    "Again, the main task is to add CSV export to the current analytics table."
)

VERSIONS = {
    "A": """Task: Add a CSV export button to the analytics table in the existing React dashboard.

Requirements:
- Export only currently visible rows (filters and sort applied).
- Keep visible column order; exclude hidden columns.
- Dates in ISO 8601.
- No new packages/dependencies.
- Existing filtering and sorting must keep working.

Process:
1. Inspect project; list relevant files before changing code.
2. Implement.
3. Report changed files and verification steps.""",

    "B": """Task: Add CSV export button to the React analytics table.

Rules:
- Export current filtered + sorted rows only.
- Keep visible column order; exclude hidden columns.
- Dates: ISO 8601.
- No new dependencies.
- Keep existing filter/sort behavior.

Steps:
1. Inspect project; list relevant files before editing.
2. Implement.
3. Report changed files + verification steps.""",
}


REQUIRED_TERMS = {
    "CSV export":                     ["csv"],
    "Export button":                  ["button"],
    "React analytics table":          ["react", "analytics table"],
    "Filtered rows":                  ["filter"],
    "Sorted rows":                    ["sort"],
    "Visible column order":           ["column order"],
    "Exclude hidden columns":         ["hidden"],
    "ISO 8601 dates":                 ["iso 8601"],
    "No new dependency":              ["dependenc"],
    "Inspect project / list files":   ["inspect", "files"],
    "Implement":                      ["implement"],
    "Report changes + verify":        ["report", "verif"],
    "Existing filter/sort unchanged": ["existing"],
}

TARGET_BAND = (40, 60)   
WIDTH = 62


def estimate_tokens(text: str) -> int:
    """Competition method: characters / 4 (rounded)."""
    return round(len(text) / 4)


def check_requirements(prompt: str) -> list[tuple[str, bool]]:
    lower = prompt.lower()
    return [(name, all(k in lower for k in keys)) for name, keys in REQUIRED_TERMS.items()]


def analyse(prompt: str) -> dict:
    orig_tok, opt_tok = estimate_tokens(ORIGINAL_PROMPT), estimate_tokens(prompt)
    reduction = (orig_tok - opt_tok) / orig_tok * 100
    results = check_requirements(prompt)
    return {
        "chars": len(prompt),
        "tokens": opt_tok,
        "saved": orig_tok - opt_tok,
        "reduction": reduction,
        "in_band": TARGET_BAND[0] <= reduction <= TARGET_BAND[1],
        "results": results,
        "kept": sum(ok for _, ok in results),
    }


def report(label: str, prompt: str) -> dict:
    a = analyse(prompt)
    print("=" * WIDTH)
    print(f"CHALLENGE 1 - PROMPT COMPRESSION (Version {label})")
    print("Method: estimated tokens = characters / 4")
    print("=" * WIDTH)

    print("\n1) OPTIMIZED PROMPT")
    print("-" * WIDTH)
    print(prompt)
    print("-" * WIDTH)

    print(f"\n2) Original estimated tokens : {estimate_tokens(ORIGINAL_PROMPT)}   "
          f"({len(ORIGINAL_PROMPT)} chars)")
    print(f"3) Optimized estimated tokens: {a['tokens']}   ({a['chars']} chars)")
    print(f"4) Estimated reduction       : {a['reduction']:.1f}%   "
          f"[{'PASS' if a['in_band'] else 'CHECK'} - target {TARGET_BAND[0]}-{TARGET_BAND[1]}%]")
    print(f"   Tokens saved              : {a['saved']}")

    print("\n5) REQUIREMENT PRESERVATION CHECK")
    print("-" * WIDTH)
    for name, ok in a["results"]:
        print(f"  [{'OK' if ok else 'MISSING':7}] {name}")
    print("-" * WIDTH)
    print(f"  Preserved: {a['kept']}/{len(a['results'])} requirements"
          f"  -> {'ALL CONSTRAINTS KEPT' if a['kept'] == len(a['results']) else 'REVIEW NEEDED'}\n")
    return a


def comparison(stats: dict[str, dict]) -> None:
    print("=" * WIDTH)
    print("SIDE-BY-SIDE COMPARISON")
    print("=" * WIDTH)
    print(f"{'Metric':<24}{'Original':>12}" + "".join(f"{'Ver ' + k:>12}" for k in stats))
    print(f"{'Characters':<24}{len(ORIGINAL_PROMPT):>12}"
          + "".join(f"{s['chars']:>12}" for s in stats.values()))
    print(f"{'Estimated tokens':<24}{estimate_tokens(ORIGINAL_PROMPT):>12}"
          + "".join(f"{s['tokens']:>12}" for s in stats.values()))
    print(f"{'Reduction':<24}{'-':>12}"
          + "".join(f"{s['reduction']:>11.1f}%" for s in stats.values()))
    print(f"{'Requirements kept':<24}{'-':>12}"
          + "".join(f"{s['kept']}/{len(REQUIRED_TERMS):>9}" for s in stats.values()))
    print("=" * WIDTH)


def main() -> None:
    stats = {label: report(label, prompt) for label, prompt in VERSIONS.items()}
    comparison(stats)


if __name__ == "__main__":
    main()
