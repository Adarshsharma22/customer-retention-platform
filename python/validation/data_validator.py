"""
Data Validation and Quality Assurance Utility.
Provides reusable integrity checks for dataframes, schema enforcement,
range validation, and referential constraint verification.
"""

from typing import Dict, List, Tuple, Any
import pandas as pd
import numpy as np


class DataValidator:
    """Encapsulates data quality assertions and health audits."""

    @staticmethod
    def check_required_columns(df: pd.DataFrame, required: List[str]) -> Tuple[bool, List[str]]:
        missing = [col for col in required if col not in df.columns]
        return len(missing) == 0, missing

    @staticmethod
    def check_primary_key(df: pd.DataFrame, key_cols: List[str]) -> Tuple[bool, int]:
        """Validates uniqueness of single or composite primary key."""
        dup_count = df.duplicated(subset=key_cols).sum()
        null_count = df[key_cols].isnull().any(axis=1).sum()
        is_valid = (dup_count == 0) and (null_count == 0)
        return is_valid, int(dup_count + null_count)

    @staticmethod
    def check_non_negative(df: pd.DataFrame, num_cols: List[str]) -> Dict[str, int]:
        """Identifies count of negative values in designated numeric columns."""
        neg_counts = {}
        for col in num_cols:
            if col in df.columns:
                neg_counts[col] = int((df[col] < 0).sum())
        return neg_counts

    @staticmethod
    def check_date_sequence(
        df: pd.DataFrame, earlier_col: str, later_col: str
    ) -> Tuple[int, int]:
        """
        Validates logical sequence between two timestamp columns.
        Returns (valid_order_count, inverted_sequence_count).
        """
        valid_mask = df[earlier_col].notnull() & df[later_col].notnull()
        subset = df[valid_mask]
        inverted = int((subset[later_col] < subset[earlier_col]).sum())
        valid = int((subset[later_col] >= subset[earlier_col]).sum())
        return valid, inverted

    @staticmethod
    def check_foreign_key(
        child_df: pd.DataFrame,
        child_col: str,
        parent_df: pd.DataFrame,
        parent_col: str
    ) -> Tuple[bool, int]:
        """Checks for orphaned foreign key records."""
        orphans = child_df[~child_df[child_col].isin(parent_df[parent_col])][child_col].dropna()
        orphan_count = int(orphans.nunique())
        return orphan_count == 0, orphan_count
