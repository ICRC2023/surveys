"""Schema definitions for survey processing pipelines.

This module defines the abstract base class SurveySchema and supporting
dataclasses that enable schema-driven preprocessing of survey data.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable


@dataclass
class SplitColumnRule:
    """Describes a column whose values encode two levels separated by a delimiter.

    Attributes
    ----------
    source_column : str
        Column name to split (e.g., "q03")
    delimiter : str
        Separator character (e.g., "/")
    regional_column : str
        Output column name for the first level (e.g., "q03_regional")
    subregional_column : str
        Output column name for the second level (e.g., "q03_subregional")
    """

    source_column: str
    delimiter: str
    regional_column: str
    subregional_column: str


@dataclass
class BinRule:
    """Describes a pd.cut binning operation.

    Attributes
    ----------
    source_column : str
        Column name to bin (e.g., "q10")
    output_column : str
        Output column name (e.g., "q10_binned")
    bins : list
        Boundaries for binning (passed to pd.cut)
    labels : list[str]
        Category labels for bins
    right : bool, optional
        Whether intervals are right-inclusive (pd.cut parameter), by default False
    """

    source_column: str
    output_column: str
    bins: list
    labels: list[str]
    right: bool = False


@dataclass
class ClusterRule:
    """Describes a derived cluster column.

    Attributes
    ----------
    output_column : str
        Column name to create (e.g., "q01_clustered")
    description : str
        Human-readable description of the clustering logic
    apply : Callable
        Function that takes a DataFrame and returns a pd.Series
        with the derived cluster values. Use named static methods
        on the concrete schema class for testability and clarity.
    """

    output_column: str
    description: str
    apply: Callable  # Callable[[pd.DataFrame], pd.Series]


class SurveySchema(ABC):
    """Abstract base class for survey-specific configuration.

    Subclasses define all survey-specific preprocessing rules. The generic
    SurveyProcessor delegates to these rules without knowing survey specifics.

    Class-level attributes (override in subclass):
    - categorical_headers: Column names of categorical type
    - numerical_headers: Column names of numerical type
    - free_text_columns: Column names containing free-text responses

    Examples
    --------
    Define a concrete schema for your survey by inheriting from SurveySchema
    and implementing all abstract methods:

    >>> class MySchema(SurveySchema):
    ...     categorical_headers = ["q01", "q02", "q03"]
    ...     free_text_columns = ["q15", "q16"]
    ...
    ...     def get_replace_rules(self):
    ...         return {"q01": {"old": "new"}}
    ...
    ...     def get_split_rules(self):
    ...         return [SplitColumnRule("geo", "/", "geo_r", "geo_s")]
    ...
    ...     def get_cluster_rules(self):
    ...         return [ClusterRule("clustered", "desc", self._cluster_q01)]
    ...
    ...     def get_bin_rules(self):
    ...         return [BinRule("num", "binned", [-1, 0, 10], ["low", "high"])]
    ...
    ...     @staticmethod
    ...     def _cluster_q01(df):
    ...         return pd.Series("C1", index=df.index)
    """

    categorical_headers: list[str] = []
    numerical_headers: list[str] = []
    free_text_columns: list[str] = []

    @abstractmethod
    def get_replace_rules(self) -> dict[str, dict]:
        """Return column-level value replacement rules.

        Returns
        -------
        dict[str, dict]
            Outer key: column name. Inner dict: {old_value: new_value}.
            Example: {"q03": {"Oceania": "Oceania / Oceania"}}
        """

    @abstractmethod
    def get_split_rules(self) -> list[SplitColumnRule]:
        """Return rules for splitting composite columns.

        Returns
        -------
        list[SplitColumnRule]
            Each rule describes a column to split on a delimiter
            and the output column names.
        """

    @abstractmethod
    def get_cluster_rules(self) -> list[ClusterRule]:
        """Return cluster derivation rules.

        Returns
        -------
        list[ClusterRule]
            Each rule carries an `apply` callable that accepts
            the full DataFrame and returns a pd.Series (the new column).
        """

    @abstractmethod
    def get_bin_rules(self) -> list[BinRule]:
        """Return binning rules for numerical columns.

        Returns
        -------
        list[BinRule]
            Each rule specifies a column to bin, boundaries, and labels.
        """
