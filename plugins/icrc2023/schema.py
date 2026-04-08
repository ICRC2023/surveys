"""ICRC2023 survey schema plugin.

Implements survey-specific configuration for the ICRC2023 diversity session survey.
"""

from __future__ import annotations

import pandas as pd

from titanite.core import BinRule, ClusterRule, SplitColumnRule, SurveySchema


class ICRC2023Schema(SurveySchema):
    """Schema for ICRC2023 Diversity Session survey.

    Defines survey-specific:
    - value replacements (q03, q04, q14)
    - geographic splitting (q03, q04)
    - clustering rules (4 derived columns)
    - binning rules (q10, q13)

    This schema extracts and generalizes the survey-specific logic
    from the original preprocess.py functions.
    """

    categorical_headers = [
        "q01", "q02", "q03", "q03_regional", "q03_subregional",
        "q04", "q04_regional", "q04_subregional",
        "q05", "q06", "q07", "q08", "q09", "q11",
        "q12_genderbalance", "q12_diversity", "q12_equity", "q12_inclusion",
        "q14", "q17_genderbalance", "q17_diversity", "q17_equity", "q17_inclusion",
        "q19", "q01_clustered", "q01q02_clustered", "q13q14_clustered",
    ]

    numerical_headers = ["q10", "q13"]

    free_text_columns = ["q15", "q16", "q18", "q20", "q21", "q22"]

    def get_replace_rules(self) -> dict[str, dict]:
        """Return value replacement rules for q03, q04, q14.

        These replacements standardize survey responses that need special handling.
        """
        return {
            "q03": {
                "Prefer not to answer": "Prefer not to answer / Prefer not to answer",
                "Oceania": "Oceania / Oceania",
            },
            "q04": {
                "Prefer not to answer": "Prefer not to answer / Prefer not to answer",
                "Oceania": "Oceania / Oceania",
            },
            "q14": {
                "No Interest": "No interest",
            },
        }

    def get_split_rules(self) -> list[SplitColumnRule]:
        """Return geographic splitting rules.

        q03 (work location) and q04 (origin) are split into
        regional and subregional components.
        """
        return [
            SplitColumnRule(
                source_column="q03",
                delimiter="/",
                regional_column="q03_regional",
                subregional_column="q03_subregional",
            ),
            SplitColumnRule(
                source_column="q04",
                delimiter="/",
                regional_column="q04_regional",
                subregional_column="q04_subregional",
            ),
        ]

    def get_cluster_rules(self) -> list[ClusterRule]:
        """Return clustering rules.

        Four derived cluster columns:
        - q01_clustered: age-based (under 40s vs 40+)
        - q13_clustered: female ratio (<=20% vs >=40%)
        - q01q02_clustered: young female/male
        - q13q14_clustered: ratio-satisfaction
        """
        return [
            ClusterRule(
                output_column="q01_clustered",
                description="Age cluster: Cluster1 (under 40s) vs Cluster2 (40s and over)",
                apply=self._cluster_q01,
            ),
            ClusterRule(
                output_column="q13_clustered",
                description="Female ratio cluster: Cluster1 (<=20%) vs Cluster2 (>=40%)",
                apply=self._cluster_q13,
            ),
            ClusterRule(
                output_column="q01q02_clustered",
                description="Young female/male: Cluster1 (under 40s, Female) vs Cluster2 (under 40s, Male)",
                apply=self._cluster_q01q02,
            ),
            ClusterRule(
                output_column="q13q14_clustered",
                description="Ratio-satisfaction: Cluster1 (<25%, Poor/Very Poor) vs Cluster2 (>25%, Good/Very Good)",
                apply=self._cluster_q13q14,
            ),
        ]

    def get_bin_rules(self) -> list[BinRule]:
        """Return binning rules.

        q10: number of invited speakers
        q13: female ratio (percentage)
        """
        return [
            BinRule(
                source_column="q10",
                output_column="q10_binned",
                bins=[-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 25],
                labels=[
                    "Prefer not to answer", "0", "1", "2", "3", "4", "5",
                    "6", "7", "8", "9", "10+",
                ],
                right=False,
            ),
            BinRule(
                source_column="q13",
                output_column="q13_binned",
                bins=[
                    -1, 0, 10, 15, 20, 25, 30, 35, 40, 45, 50,
                    55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105,
                ],
                labels=[
                    "Prefer not to answer", "0%", "10%", "15%", "20%", "25%", "30%",
                    "35%", "40%", "45%", "50%", "55%", "60%", "65%", "70%",
                    "75%", "80%", "85%", "90%", "95%", "100%",
                ],
                right=False,
            ),
        ]

    @staticmethod
    def _cluster_q01(df: pd.DataFrame) -> pd.Series:
        """Age cluster: Cluster1 (under 40s) vs Cluster2 (40s and over)."""
        result = pd.Series("Others", index=df.index, dtype=str)
        result[df["q01"] < "40s"] = "Cluster1"
        result[df["q01"] >= "40s"] = "Cluster2"
        return result

    @staticmethod
    def _cluster_q13(df: pd.DataFrame) -> pd.Series:
        """Female ratio cluster: Cluster1 (<=20%) vs Cluster2 (>=40%)."""
        result = pd.Series("Others", index=df.index, dtype=str)
        result[df["q13"] <= 20] = "Cluster1"
        result[df["q13"] >= 40] = "Cluster2"
        return result

    @staticmethod
    def _cluster_q01q02(df: pd.DataFrame) -> pd.Series:
        """Young female/male: Cluster1 (under 40s, Female) vs Cluster2 (under 40s, Male)."""
        result = pd.Series("Others", index=df.index, dtype=str)
        is_young_female = (df["q01"] < "40s") & (df["q02"] == "Female")
        result[is_young_female] = "Cluster1"
        is_young_male = (df["q01"] < "40s") & (df["q02"] == "Male")
        result[is_young_male] = "Cluster2"
        return result

    @staticmethod
    def _cluster_q13q14(df: pd.DataFrame) -> pd.Series:
        """Ratio-satisfaction: Cluster1 (<25%, Poor/Very Poor) vs Cluster2 (>25%, Good/Very Good)."""
        result = pd.Series("Others", index=df.index, dtype=str)
        is_poor_ratio = (df["q13"] < 25) & (df["q14"].isin(["Very Poor", "Poor"]))
        result[is_poor_ratio] = "Cluster1"
        is_good_ratio = (df["q13"] > 25) & (df["q14"].isin(["Very Good", "Good"]))
        result[is_good_ratio] = "Cluster2"
        return result
