"""Tests for data generation, preprocessing, and validation modules."""

import numpy as np
import pandas as pd
import pytest

from src.data.generate_data import generate_manufacturing_data
from src.data.validate import (
    validate_data,
    validate_no_nulls,
    validate_ranges,
    validate_schema,
)


class TestGenerateData:
    def test_generates_correct_number_of_samples(self):
        df = generate_manufacturing_data(num_samples=100, seed=42)
        assert len(df) == 100

    def test_has_all_expected_columns(self):
        df = generate_manufacturing_data(num_samples=50, seed=42)
        expected = [
            "temperature", "pressure", "vibration", "humidity", "speed",
            "thickness", "power_consumption", "tool_wear", "coolant_flow",
            "ambient_temp", "cycle_time", "material_hardness", "spindle_load",
            "feed_rate", "surface_roughness", "quality_score",
        ]
        assert list(df.columns) == expected

    def test_quality_score_bounded(self):
        df = generate_manufacturing_data(num_samples=1000, seed=42)
        assert df["quality_score"].min() >= 0
        assert df["quality_score"].max() <= 100

    def test_reproducible_with_same_seed(self):
        df1 = generate_manufacturing_data(num_samples=50, seed=42)
        df2 = generate_manufacturing_data(num_samples=50, seed=42)
        pd.testing.assert_frame_equal(df1, df2)

    def test_different_seeds_produce_different_data(self):
        df1 = generate_manufacturing_data(num_samples=50, seed=42)
        df2 = generate_manufacturing_data(num_samples=50, seed=99)
        assert not df1.equals(df2)


class TestValidation:
    @pytest.fixture
    def valid_df(self):
        return generate_manufacturing_data(num_samples=100, seed=42)

    def test_valid_data_passes_all_checks(self, valid_df):
        assert validate_data(valid_df) is True

    def test_missing_column_fails_schema(self, valid_df):
        df = valid_df.drop(columns=["temperature"])
        with pytest.raises(ValueError, match="Missing required columns"):
            validate_schema(df)

    def test_null_values_fail_validation(self, valid_df):
        df = valid_df.copy()
        df.loc[0, "temperature"] = None
        with pytest.raises(ValueError, match="Null values found"):
            validate_no_nulls(df)

    def test_out_of_range_fails(self):
        df = generate_manufacturing_data(num_samples=10, seed=42)
        df.loc[0, "temperature"] = 999  # way out of range
        with pytest.raises(ValueError, match="Range violations"):
            validate_ranges(df)
