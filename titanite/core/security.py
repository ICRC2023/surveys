"""Privacy-safe handling of sensitive survey data.

This module provides utilities for protecting survey response confidentiality
during aggregation and publication.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from loguru import logger


class SecureDataHandler:
    """Utilities for privacy-safe data operations.

    All methods are static — no instance state needed.
    Focuses on:

    - Safe data loading
    - Cell suppression (n < threshold removal, for aggregated data)
    - k-anonymization (row suppression, for individual-level data)
    - Timestamp generalization (precision reduction)
    - Anonymization (sensitive column removal)
    - build_public_dataset: the full individual-level publication pipeline

    Examples
    --------
    >>> df = SecureDataHandler.load_sensitive_data("prepared_data.csv")
    >>> public = SecureDataHandler.build_public_dataset(
    ...     df,
    ...     free_text_columns=["q15", "q16"],
    ...     quasi_identifiers=["q01", "q02", "q03_subregional", "q05"],
    ...     k=5,
    ... )
    """

    @staticmethod
    def load_sensitive_data(filepath: str | Path) -> pd.DataFrame:
        """Load a CSV file safely (read-only, no side effects).

        Parameters
        ----------
        filepath : str or Path
            Path to the CSV file to load

        Returns
        -------
        pd.DataFrame
            Loaded data

        Raises
        ------
        FileNotFoundError
            If the file does not exist
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Data file not found: {path}")
        logger.info(f"Loading sensitive data from: {path}")
        data = pd.read_csv(path)
        return data

    @staticmethod
    def suppress_small_cells(
        data: pd.DataFrame,
        threshold: int = 5,
        count_column: str = "count",
    ) -> pd.DataFrame:
        """Apply cell suppression: remove rows where count < threshold.

        Used to prevent individual identification in aggregated results.
        This is essential for privacy protection in statistical releases.

        Parameters
        ----------
        data : pd.DataFrame
            Aggregated (crosstab or grouped) DataFrame
        threshold : int, optional
            Minimum cell count to retain, by default 5
        count_column : str, optional
            Name of the column holding counts, by default "count"

        Returns
        -------
        pd.DataFrame
            Filtered DataFrame with small cells removed. If count_column
            is not found, returns data unchanged with a warning.
        """
        if count_column not in data.columns:
            logger.warning(
                f"Column '{count_column}' not found in data; suppression not applied"
            )
            return data
        return data[data[count_column] >= threshold].copy()

    @staticmethod
    def aggregate_counts(
        data: pd.DataFrame,
        columns: list[str],
        threshold: int = 5,
        count_column: str = "count",
    ) -> pd.DataFrame:
        """Build a suppressed frequency table from individual-level data.

        Groups the rows by ``columns`` and counts them, then drops every
        combination seen fewer than ``threshold`` times. The result is safe
        to publish: it carries only category values and counts, and no cell
        represents a group small enough to single out a respondent.

        Parameters
        ----------
        data : pd.DataFrame
            Individual-level (one row per respondent) DataFrame
        columns : list[str]
            One or two column names to cross-tabulate (e.g. ["q03_subregional"]
            or ["q03_subregional", "q02"])
        threshold : int, optional
            Minimum count to retain a row, by default 5
        count_column : str, optional
            Name of the count column in the output, by default "count"

        Returns
        -------
        pd.DataFrame
            Long-format frequency table: one row per surviving combination,
            with the group columns plus ``count_column``. Empty if no
            combination reaches ``threshold``.
        """
        present = [c for c in columns if c in data.columns]
        missing = [c for c in columns if c not in data.columns]
        if missing:
            logger.warning(f"Columns not found, skipped: {missing}")
        if not present:
            return pd.DataFrame(columns=[*columns, count_column])
        counts = (
            data.groupby(present, dropna=False, observed=True)
            .size()
            .reset_index(name=count_column)
        )
        return SecureDataHandler.suppress_small_cells(
            counts, threshold=threshold, count_column=count_column
        )

    @staticmethod
    def generalize_timestamp(
        data: pd.DataFrame,
        column: str = "timestamp",
        freq: str = "D",
    ) -> pd.DataFrame:
        """Reduce timestamp precision by truncating to a coarser frequency.

        A second-level response timestamp is a quasi-identifier: it can be
        matched against mailing logs or event schedules to re-identify a
        respondent. Truncating to daily (or coarser) granularity removes that
        risk while keeping the timeline usable for aggregate response plots.

        Parameters
        ----------
        data : pd.DataFrame
            DataFrame containing the timestamp column
        column : str, optional
            Name of the timestamp column, by default "timestamp"
        freq : str, optional
            Target resolution as a pandas offset alias (e.g. "D" for day,
            "h" for hour, "W" for week), by default "D"

        Returns
        -------
        pd.DataFrame
            Copy of data with the timestamp column truncated. If the column
            is not present, returns data unchanged with a warning.
        """
        if column not in data.columns:
            logger.warning(
                f"Column '{column}' not found in data; timestamp not generalized"
            )
            return data.copy()
        result = data.copy()
        result[column] = pd.to_datetime(result[column]).dt.floor(freq)
        return result

    @staticmethod
    def k_anonymize(
        data: pd.DataFrame,
        quasi_identifiers: list[str],
        k: int = 5,
    ) -> pd.DataFrame:
        """Enforce k-anonymity on individual-level records by row suppression.

        Groups rows by the combination of quasi-identifier values and drops
        every group whose size is smaller than ``k``. After this, no
        respondent can be singled out by any combination of the given
        quasi-identifiers plus outside knowledge (e.g. a public attendee
        list): each surviving combination is shared by at least ``k`` people.

        Parameters
        ----------
        data : pd.DataFrame
            Individual-level (one row per respondent) DataFrame
        quasi_identifiers : list[str]
            Column names that could be linked against external data
            (e.g. ["q01", "q02", "q03_subregional", "q05"])
        k : int, optional
            Minimum group size to retain, by default 5

        Returns
        -------
        pd.DataFrame
            Copy of data containing only rows whose quasi-identifier
            combination occurs at least ``k`` times. If none of the
            quasi-identifier columns are present, returns data unchanged
            with a warning.
        """
        present = [c for c in quasi_identifiers if c in data.columns]
        if not present:
            logger.warning(
                "None of the quasi-identifier columns found in data; "
                "k-anonymization not applied"
            )
            return data.copy()
        if len(present) < len(quasi_identifiers):
            missing = [c for c in quasi_identifiers if c not in data.columns]
            logger.warning(f"Quasi-identifier columns not found: {missing}")
        group_sizes = data.groupby(present, dropna=False)[present[0]].transform("size")
        mask = group_sizes >= k
        dropped = int((~mask).sum())
        if dropped:
            logger.info(
                f"k-anonymization (k={k}): dropped {dropped} rows, "
                f"{int(mask.sum())} rows retained"
            )
        return data[mask].copy()

    @staticmethod
    def anonymize_for_publication(
        data: pd.DataFrame,
        sensitive_columns: list[str],
    ) -> pd.DataFrame:
        """Remove sensitive columns before publication.

        Strips personally identifiable information and free-text responses
        that could compromise respondent confidentiality.

        Parameters
        ----------
        data : pd.DataFrame
            DataFrame to anonymize
        sensitive_columns : list[str]
            Column names to remove (e.g., ["timestamp", "q15", "q16"])

        Returns
        -------
        pd.DataFrame
            Copy of data with sensitive columns dropped (if they exist)
        """
        columns_to_drop = [c for c in sensitive_columns if c in data.columns]
        if columns_to_drop:
            logger.info(f"Dropping sensitive columns: {columns_to_drop}")
        return data.drop(columns=columns_to_drop).copy()

    @staticmethod
    def build_public_dataset(
        data: pd.DataFrame,
        free_text_columns: list[str],
        quasi_identifiers: list[str],
        k: int = 5,
        timestamp_column: str = "timestamp",
        timestamp_freq: str = "D",
        translation_suffix: str = "_ja",
        extra_drop_columns: list[str] | None = None,
    ) -> pd.DataFrame:
        """Turn an individual-level DataFrame into a publication-safe dataset.

        Combines the lower-level privacy operations into the full pipeline
        used by ``ti anonymize``:

        1. Drop free-text response columns and their translations
           (e.g. "q15" and "q15_ja"). Their sentiment scores
           (e.g. "q15_polarity") are non-reversible aggregates and are kept.
        2. Truncate the timestamp column to a coarser resolution.
        3. Enforce k-anonymity on the quasi-identifier combination.

        Parameters
        ----------
        data : pd.DataFrame
            Individual-level (one row per respondent) DataFrame, typically
            loaded from ``prepared_data.csv``
        free_text_columns : list[str]
            Free-text response column names (e.g. ["q15", "q16", ...]).
            For each name, ``name`` and ``name + translation_suffix`` are
            dropped if present.
        quasi_identifiers : list[str]
            Columns to protect via k-anonymity (see :meth:`k_anonymize`)
        k : int, optional
            Minimum group size for k-anonymity, by default 5
        timestamp_column : str, optional
            Timestamp column to generalize, by default "timestamp"
        timestamp_freq : str, optional
            Target timestamp resolution, by default "D" (daily)
        translation_suffix : str, optional
            Suffix identifying translated free-text columns, by default "_ja"
        extra_drop_columns : list[str] or None, optional
            Additional columns to drop (e.g. ["response"]), by default None

        Returns
        -------
        pd.DataFrame
            Publication-safe copy: no free-text, coarsened timestamp, and
            every quasi-identifier combination shared by at least ``k``
            respondents.
        """
        drop_columns = []
        for column in free_text_columns:
            drop_columns.append(column)
            drop_columns.append(f"{column}{translation_suffix}")
        if extra_drop_columns:
            drop_columns.extend(extra_drop_columns)

        result = SecureDataHandler.anonymize_for_publication(data, drop_columns)
        result = SecureDataHandler.generalize_timestamp(
            result, column=timestamp_column, freq=timestamp_freq
        )
        result = SecureDataHandler.k_anonymize(
            result, quasi_identifiers=quasi_identifiers, k=k
        )
        return result
