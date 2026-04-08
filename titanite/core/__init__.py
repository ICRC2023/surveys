"""titanite.core — Generic survey processing framework

This subpackage provides the abstract schema-based framework for building
reusable survey data processing pipelines.

Main exports:
- SurveySchema: Abstract base class for survey-specific configuration
- SurveyProcessor: Schema-driven preprocessing pipeline
- SecureDataHandler: Privacy-safe data operations
"""

from .processor import SurveyProcessor
from .schema import SurveySchema, SplitColumnRule, ClusterRule, BinRule
from .security import SecureDataHandler

__all__ = [
    "SurveySchema",
    "SurveyProcessor",
    "SecureDataHandler",
    "SplitColumnRule",
    "ClusterRule",
    "BinRule",
]
