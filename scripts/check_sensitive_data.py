#!/usr/bin/env python3
"""Fail if individual-level survey data is tracked in git.

Used by CI (.github/workflows/quality.yml) and by a pre-commit hook. The
check is content-based rather than path-based: a data file is treated as
sensitive if it is a CSV/TSV/JSON whose header (CSV/TSV) or first record
(JSON) contains a free-text response column or its ``_ja`` translation.
This blocks the individual-level ``data/private/`` extract and any stray
raw export, while allowing the anonymized, aggregated ``data/public/``
files (which carry only counts and sentiment scores).

Exit code 0 = clean, 1 = sensitive file tracked (or a listed path is
unreadable).
"""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

# Free-text response columns for the ICRC2023 survey. A CSV/JSON carrying
# any of these (or "<name>_ja") holds verbatim answers and must not be
# committed. Keep in sync with plugins/icrc2023/schema.py free_text_columns.
FREE_TEXT_COLUMNS = ["q15", "q16", "q18", "q20", "q21", "q22"]
SENSITIVE_COLUMN_NAMES = set(FREE_TEXT_COLUMNS) | {f"{c}_ja" for c in FREE_TEXT_COLUMNS}

DATA_SUFFIXES = {".csv", ".tsv", ".json"}


def _tracked_data_files() -> list[str]:
    """Return git-tracked files under data/ with a data suffix."""
    out = subprocess.run(
        ["git", "ls-files", "-z", "data/"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    files = [p for p in out.split("\0") if p]
    return [f for f in files if Path(f).suffix.lower() in DATA_SUFFIXES]


def _columns_of(path: Path) -> set[str]:
    """Return the set of column / field names in a CSV, TSV or JSON file."""
    suffix = path.suffix.lower()
    if suffix in {".csv", ".tsv"}:
        delimiter = "\t" if suffix == ".tsv" else ","
        with path.open(newline="", encoding="utf-8", errors="replace") as fh:
            reader = csv.reader(fh, delimiter=delimiter)
            header = next(reader, [])
        return {c.strip() for c in header}
    # JSON: list of records, or a dict of columns
    with path.open(encoding="utf-8", errors="replace") as fh:
        data = json.load(fh)
    if isinstance(data, list) and data and isinstance(data[0], dict):
        return set(data[0].keys())
    if isinstance(data, dict):
        return set(data.keys())
    return set()


def main(argv: list[str]) -> int:
    # pre-commit passes the staged file list; without args, check everything
    # git currently tracks under data/.
    candidates = argv or _tracked_data_files()
    candidates = [c for c in candidates if Path(c).suffix.lower() in DATA_SUFFIXES]

    offenders: list[str] = []
    errors: list[str] = []
    for name in candidates:
        path = Path(name)
        if not path.exists():
            continue
        try:
            columns = _columns_of(path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"{name}: could not inspect ({exc})")
            continue
        leaked = sorted(columns & SENSITIVE_COLUMN_NAMES)
        if leaked:
            offenders.append(f"{name}: free-text columns {leaked}")

    if errors:
        print("Could not inspect some data files:")
        for e in errors:
            print(f"  - {e}")

    if offenders:
        print(
            "\nERROR: individual-level survey data is tracked in git.\n"
            "These files carry verbatim free-text answers and must not be "
            "committed:\n"
        )
        for o in offenders:
            print(f"  - {o}")
        print(
            "\nKeep individual-level data in data/private/ (git-ignored). "
            "Publish only the anonymized data/public/ extract from "
            "`ti anonymize`. See PLAN.md Phase 5.\n"
        )
        return 1

    if errors:
        return 1

    print("OK: no individual-level survey data tracked in git.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
