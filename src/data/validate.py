"""Data validation using Great Expectations.

Defines and runs expectation suites to ensure data quality
before model training.
"""

import logging
from typing import Dict, List

import pandas as pd

logger = logging.getLogger(__name__)

# Expected value ranges for manufacturing features
FEATURE_RANGES: Dict[str, Dict[str, float]] = {
    "temperature": {"min": 100, "max": 300},
    "pressure": {"min": 20, "max": 80},
    "vibration": {"min": 0, "max": 1.0},
    "humidity": {"min": 10, "max": 100},
    "speed": {"min": 500, "max": 2000},
    "thickness": {"min": 0.5, "max": 5.0},
    "power_consumption": {"min": 200, "max": 500},
    "tool_wear": {"min": 0, "max": 1.0},
    "coolant_flow": {"min": 0, "max": 20},
    "ambient_temp": {"min": 10, "max": 45},
    "cycle_time": {"min": 20, "max": 80},
    "material_hardness": {"min": 30, "max": 80},
    "spindle_load": {"min": 20, "max": 100},
    "feed_rate": {"min": 0.05, "max": 0.5},
    "surface_roughness": {"min": 0, "max": 20},
    "quality_score": {"min": 0, "max": 100},
}

REQUIRED_COLUMNS: List[str] = list(FEATURE_RANGES.keys())


def validate_schema(df: pd.DataFrame) -> bool:
    """Check that all required columns are present.

    Args:
        df: DataFrame to validate.

    Returns:
        True if all required columns exist.

    Raises:
        ValueError: If required columns are missing.
    """
    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    logger.info("Schema validation passed")
    return True


def validate_no_nulls(df: pd.DataFrame) -> bool:
    """Check for null values in the dataset.

    Args:
        df: DataFrame to validate.

    Returns:
        True if no nulls found.

    Raises:
        ValueError: If null values are found.
    """
    null_counts = df[REQUIRED_COLUMNS].isnull().sum()
    cols_with_nulls = null_counts[null_counts > 0]
    if len(cols_with_nulls) > 0:
        raise ValueError(f"Null values found: {cols_with_nulls.to_dict()}")
    logger.info("Null validation passed")
    return True


def validate_ranges(df: pd.DataFrame) -> bool:
    """Check that feature values fall within expected physical ranges.

    Args:
        df: DataFrame to validate.

    Returns:
        True if all values are within range.

    Raises:
        ValueError: If out-of-range values are found.
    """
    violations = []
    for col, bounds in FEATURE_RANGES.items():
        if col not in df.columns:
            continue
        below = (df[col] < bounds["min"]).sum()
        above = (df[col] > bounds["max"]).sum()
        if below > 0 or above > 0:
            violations.append(f"{col}: {below} below min, {above} above max")

    if violations:
        raise ValueError(f"Range violations: {'; '.join(violations)}")
    logger.info("Range validation passed")
    return True


def validate_data(df: pd.DataFrame) -> bool:
    """Run all validation checks on the dataset.

    Args:
        df: DataFrame to validate.

    Returns:
        True if all checks pass.
    """
    validate_schema(df)
    validate_no_nulls(df)
    validate_ranges(df)
    logger.info("All data validations passed")
    return True
