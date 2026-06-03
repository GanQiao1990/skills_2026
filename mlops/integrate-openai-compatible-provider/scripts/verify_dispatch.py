#!/usr/bin/env python3
"""Verify all dispatch points in AI-Scientist-v2 have a given provider branch.

Usage: python verify_dispatch.py mimo
"""
import sys
import re
from pathlib import Path

PROVIDER = sys.argv[1] if len(sys.argv) > 1 else "mimo"

FILES_TO_CHECK = [
    "ai_scientist/llm.py",
    "ai_scientist/vlm.py",
    "ai_scientist/treesearch/backend/backend_openai.py",
]

def check_file(filepath, provider):
    """Check that every 'else raise ValueError.*not supported' has the provider branch above it."""
    path = Path(filepath)
    if not path.exists():
        print(f"  SKIP {filepath} (not found)")
        return True

    lines = path.read_text().splitlines()
    ok = True
    for i, line in enumerate(lines):
        if "not supported" in line and "raise" in line:
            # Look backwards for the provider branch
            found = False
            for j in range(i - 1, max(0, i - 15), -1):
                if provider in lines[j]:
                    found = True
                    break
                # Stop at previous elif/else/if
                if lines[j].strip().startswith(("if ", "elif ", "else:")) and provider not in lines[j]:
                    # Check if this is the start of a different branch
                    if j < i - 1:  # Only if there's room
                        break
            if not found:
                print(f"  MISSING {filepath}:{i+1} — no '{provider}' branch before 'raise ValueError'")
                ok = False
            else:
                print(f"  OK {filepath}:{i+1}")
    return ok


def check_available_lists(provider):
    """Check AVAILABLE_LLMS and AVAILABLE_VLMS contain the provider."""
    ok = True
    for filepath, varname in [
        ("ai_scientist/llm.py", "AVAILABLE_LLMS"),
        ("ai_scientist/vlm.py", "AVAILABLE_VLMS"),
    ]:
        path = Path(filepath)
        if not path.exists():
            continue
        content = path.read_text()
        if varname in content and provider in content:
            print(f"  OK {filepath} — {varname} contains '{provider}'")
        elif varname in content:
            print(f"  MISSING {filepath} — {varname} does NOT contain '{provider}'")
            ok = False
    return ok


def check_dotenv():
    """Check dotenv loading in key files."""
    ok = True
    for filepath in FILES_TO_CHECK + ["launch_scientist_bfts.py"]:
        path = Path(filepath)
        if not path.exists():
            continue
        content = path.read_text()
        if "load_dotenv" in content:
            print(f"  OK {filepath} — has dotenv")
        else:
            print(f"  WARN {filepath} — no dotenv loading")
    return ok


if __name__ == "__main__":
    print(f"=== Verifying provider '{PROVIDER}' ===\n")

    print("1. Dispatch branches:")
    all_ok = True
    for f in FILES_TO_CHECK:
        all_ok &= check_file(f, PROVIDER)

    print("\n2. AVAILABLE_* lists:")
    all_ok &= check_available_lists(PROVIDER)

    print("\n3. dotenv loading:")
    check_dotenv()

    print(f"\n{'PASS' if all_ok else 'FAIL'}")
    sys.exit(0 if all_ok else 1)
