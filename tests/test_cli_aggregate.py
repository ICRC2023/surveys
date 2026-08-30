"""Tests for the `ti aggregate` CLI command."""

import csv

import pandas as pd
from typer.testing import CliRunner

from titanite.cli import app

runner = CliRunner()


def _make_prepared_csv(path):
    """Individual-level CSV: q02 has a rare Non-binary group (n=3)."""
    df = pd.DataFrame(
        {
            "q01": ["20s"] * 10 + ["30s"] * 10,
            "q02": ["Male"] * 9 + ["Female"] * 8 + ["Non-binary"] * 3,
            "q15": ["verbatim answer"] * 20,
        }
    )
    df.to_csv(path, index=False)


def test_aggregate_writes_suppressed_univariate_tables(tmp_path):
    """Each categorical header gets a univariate CSV with small cells removed."""
    read_from = tmp_path / "prepared_data.csv"
    write_dir = tmp_path / "aggregates"
    _make_prepared_csv(read_from)

    result = runner.invoke(
        app,
        [
            "aggregate",
            "--read-from",
            str(read_from),
            "--write-dir",
            str(write_dir),
            "--threshold",
            "5",
        ],
    )
    assert result.exit_code == 0

    q02 = write_dir / "univariate" / "q02.csv"
    assert q02.exists()
    with q02.open() as f:
        rows = list(csv.DictReader(f))
    labels = {r["q02"] for r in rows}
    # Male (9) and Female (8) survive; Non-binary (3) is suppressed.
    assert labels == {"Male", "Female"}
    assert set(rows[0].keys()) == {"q02", "count"}

    # Free-text columns are never aggregated.
    assert not (write_dir / "univariate" / "q15.csv").exists()


def test_aggregate_pair_option_writes_bivariate_table(tmp_path):
    """--pair X,Y produces a cross-tab CSV under bivariate/."""
    read_from = tmp_path / "prepared_data.csv"
    write_dir = tmp_path / "aggregates"
    _make_prepared_csv(read_from)

    result = runner.invoke(
        app,
        [
            "aggregate",
            "--read-from",
            str(read_from),
            "--write-dir",
            str(write_dir),
            "--pair",
            "q01,q02",
            "--threshold",
            "1",
        ],
    )
    assert result.exit_code == 0

    out = write_dir / "bivariate" / "q01__q02.csv"
    assert out.exists()
    with out.open() as f:
        rows = list(csv.DictReader(f))
    assert set(rows[0].keys()) == {"q01", "q02", "count"}
    total = sum(int(r["count"]) for r in rows)
    assert total == 20
