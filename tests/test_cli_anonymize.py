"""Tests for the `ti anonymize` CLI command."""

import csv
from collections import Counter

import pandas as pd
from typer.testing import CliRunner

from plugins.icrc2023 import ICRC2023Schema
from titanite.cli import app

runner = CliRunner()


def _make_prepared_csv(path):
    """Write a synthetic prepared_data.csv with the columns anonymize touches.

    Six ("20s", "Female", "Europe") rows survive k=5; two rare rows do not.
    """
    base_rows = 6
    rare_rows = 2
    df = pd.DataFrame(
        {
            "timestamp": ["2023-07-15 10:23:45"] * base_rows
            + ["2023-07-16 08:00:00"] * rare_rows,
            "q01": ["20s"] * base_rows + ["90s+"] * rare_rows,
            "q02": ["Female"] * base_rows + ["Non-binary"] * rare_rows,
            "q03": ["Europe / West"] * (base_rows + rare_rows),
            "q03_regional": ["Europe"] * base_rows + ["Oceania"] * rare_rows,
            "q03_subregional": ["West Europe"] * base_rows + ["Oceania"] * rare_rows,
            "q05": ["Postdoc"] * (base_rows + rare_rows),
            "q15": ["free text response"] * (base_rows + rare_rows),
            "q15_ja": ["自由記述"] * (base_rows + rare_rows),
            "q15_polarity": [0.25] * (base_rows + rare_rows),
            "q15_subjectivity": [0.5] * (base_rows + rare_rows),
            "response": [1] * (base_rows + rare_rows),
        }
    )
    df.to_csv(path, index=False)


def test_anonymize_help_lists_options():
    """anonymize command exposes its documented options."""
    result = runner.invoke(app, ["anonymize", "--help"])
    assert result.exit_code == 0
    assert "--plugin" in result.stdout
    assert "--k" in result.stdout


def test_anonymize_produces_public_dataset(tmp_path):
    """anonymize removes sensitive columns, coarsens time, and k-anonymizes."""
    read_from = tmp_path / "prepared_data.csv"
    write_dir = tmp_path / "public"
    write_dir.mkdir()
    _make_prepared_csv(read_from)

    result = runner.invoke(
        app,
        [
            "anonymize",
            "--read-from",
            str(read_from),
            "--write-dir",
            str(write_dir),
            "--k",
            "5",
        ],
    )
    assert result.exit_code == 0

    out = write_dir / "public_data.csv"
    assert out.exists()

    with out.open() as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames
        rows = list(reader)

    # Free-text original + translation and geography finer than the
    # quasi-identifiers are gone; the sentiment score stays.
    for dropped in (
        "q15",
        "q15_ja",
        "q03",
        "q03_subregional",
        "response",
    ):
        assert dropped not in columns
    assert "q15_polarity" in columns

    # Timestamp coarsened to date only.
    assert " " not in rows[0]["timestamp"]

    # The two rare rows are suppressed; the six-row group survives.
    assert len(rows) == 6

    # No surviving quasi-identifier combination has fewer than k members.
    qi = ICRC2023Schema.quasi_identifiers
    counts = Counter(tuple(row[c] for c in qi) for row in rows)
    assert all(n >= 5 for n in counts.values())
