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
    - Cell suppression (n < threshold removal)
    - Anonymization (sensitive column removal)

    Examples
    --------
    >>> df = SecureDataHandler.load_sensitive_data("data.csv")
    >>> suppressed = SecureDataHandler.suppress_small_cells(df, threshold=5)
    >>> safe = SecureDataHandler.anonymize_for_publication(
    ...     suppressed, sensitive_columns=["timestamp", "q15"]
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
