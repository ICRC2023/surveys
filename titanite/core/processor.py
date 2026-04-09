"""Survey data processing pipeline driven by schema configuration.

The SurveyProcessor class orchestrates preprocessing steps according to
a SurveySchema, enabling reusable, pluggable survey data pipelines.
"""

from __future__ import annotations

import pandas as pd
from loguru import logger

from .schema import SurveySchema


class SurveyProcessor:
    """Schema-driven survey preprocessing pipeline.

    Delegates all survey-specific logic to an injected SurveySchema.
    Executes a fixed sequence of preprocessing steps: timestamp parsing,
    response counter, value replacement, geographic splitting, clustering,
    and binning.

    Attributes
    ----------
    schema : SurveySchema
        Configuration object that defines all survey-specific rules

    Examples
    --------
    >>> from titanite.core import SurveyProcessor
    >>> from my_survey import MySchema
    >>> processor = SurveyProcessor(MySchema())
    >>> processed_df = processor.process(raw_df, config)
    """

    def __init__(self, schema: SurveySchema) -> None:
        """Initialize the processor with a survey schema.

        Parameters
        ----------
        schema : SurveySchema
            Schema instance that defines preprocessing rules
        """
        self.schema = schema

    def process(self, df: pd.DataFrame, config=None) -> pd.DataFrame:
        """Run the full preprocessing pipeline.

        Parameters
        ----------
        df : pd.DataFrame
            Raw survey DataFrame (post CSV load, pre-processing)
        config : optional
            Configuration object (reserved for Phase 2 categorization step)

        Returns
        -------
        pd.DataFrame
            Fully preprocessed DataFrame with derived columns
        """
        logger.info(f"SurveyProcessor: starting pipeline on {len(df)} rows")
        df = df.copy()  # Avoid SettingWithCopyWarning on DataFrame slices
        df = self._add_timestamp(df)
        df = self._add_response_counter(df)
        df = self._apply_replace_rules(df)
        df = self._split_geographic_data(df)
        df = self._apply_cluster_rules(df)
        df = self._apply_bin_rules(df)
        logger.info("SurveyProcessor: pipeline complete")
        return df

    def _add_timestamp(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert timestamp column to datetime type.

        Parameters
        ----------
        df : pd.DataFrame
            Input DataFrame

        Returns
        -------
        pd.DataFrame
            DataFrame with datetime-typed timestamp column
        """
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df

    def _add_response_counter(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add a response counter column (all values = 1).

        Used for counting responses in aggregation operations.

        Parameters
        ----------
        df : pd.DataFrame
            Input DataFrame

        Returns
        -------
        pd.DataFrame
            DataFrame with added "response" column
        """
        df["response"] = 1
        return df

    def _apply_replace_rules(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply value replacement rules from the schema.

        Parameters
        ----------
        df : pd.DataFrame
            Input DataFrame

        Returns
        -------
        pd.DataFrame
            DataFrame with replaced values
        """
        rules = self.schema.get_replace_rules()
        for column, replace_map in rules.items():
            if column in df.columns:
                df[column] = df[column].replace(replace_map)
        return df

    def _split_geographic_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Split composite geographic columns based on schema rules.

        Parameters
        ----------
        df : pd.DataFrame
            Input DataFrame

        Returns
        -------
        pd.DataFrame
            DataFrame with new regional/subregional columns
        """
        for rule in self.schema.get_split_rules():
            logger.debug(
                f"Splitting {rule.source_column} → {rule.regional_column}, {rule.subregional_column}"
            )
            split = df[rule.source_column].str.split(rule.delimiter, expand=True)
            split[0] = split[0].str.strip()
            split[1] = split[1].str.strip()
            split = split.rename(
                columns={0: rule.regional_column, 1: rule.subregional_column}
            )
            df = pd.concat([df, split], axis=1)
        return df

    def _apply_cluster_rules(self, df: pd.DataFrame) -> pd.DataFrame:
        """Derive cluster columns based on schema rules.

        Parameters
        ----------
        df : pd.DataFrame
            Input DataFrame

        Returns
        -------
        pd.DataFrame
            DataFrame with new cluster columns
        """
        for rule in self.schema.get_cluster_rules():
            logger.debug(f"Applying cluster: {rule.output_column} — {rule.description}")
            df[rule.output_column] = rule.apply(df)
        return df

    def _apply_bin_rules(self, df: pd.DataFrame) -> pd.DataFrame:
        """Bin numerical columns based on schema rules.

        Parameters
        ----------
        df : pd.DataFrame
            Input DataFrame

        Returns
        -------
        pd.DataFrame
            DataFrame with new binned columns
        """
        for rule in self.schema.get_bin_rules():
            logger.debug(f"Binning {rule.source_column} → {rule.output_column}")
            df[rule.output_column] = pd.cut(
                df[rule.source_column],
                rule.bins,
                labels=rule.labels,
                right=rule.right,
            )
        return df
