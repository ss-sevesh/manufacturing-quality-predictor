"""Data preprocessing pipeline.

Handles feature scaling, train/test splitting, and scaler serialization
for consistent transformations between training and inference.
"""

import logging
import pickle
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


def load_raw_data(path: str) -> pd.DataFrame:
    """Load raw manufacturing data from CSV.

    Args:
        path: Path to the raw CSV file.

    Returns:
        Raw DataFrame.
    """
    df = pd.read_csv(path)
    logger.info(f"Loaded {len(df)} rows from {path}")
    return df


def split_features_target(
    df: pd.DataFrame, target_col: str = "quality_score"
) -> Tuple[pd.DataFrame, pd.Series]:
    """Separate features and target variable.

    Args:
        df: Input DataFrame.
        target_col: Name of the target column.

    Returns:
        Tuple of (features DataFrame, target Series).
    """
    X = df.drop(columns=[target_col])
    y = df[target_col]
    return X, y


def scale_features(
    X_train: pd.DataFrame, X_test: pd.DataFrame, scaler_path: str
) -> Tuple[np.ndarray, np.ndarray, StandardScaler]:
    """Fit StandardScaler on training data and transform both splits.

    Args:
        X_train: Training features.
        X_test: Test features.
        scaler_path: Path to save the fitted scaler.

    Returns:
        Tuple of (scaled train array, scaled test array, fitted scaler).
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    Path(scaler_path).parent.mkdir(parents=True, exist_ok=True)
    with open(scaler_path, "wb") as f:
        pickle.dump(scaler, f)
    logger.info(f"Scaler saved to {scaler_path}")

    return X_train_scaled, X_test_scaled, scaler


def load_scaler(scaler_path: str) -> StandardScaler:
    """Load a previously fitted scaler.

    Args:
        scaler_path: Path to the pickled scaler.

    Returns:
        Fitted StandardScaler instance.
    """
    with open(scaler_path, "rb") as f:
        return pickle.load(f)


def preprocess_pipeline(
    raw_path: str,
    processed_dir: str,
    scaler_path: str,
    target_col: str = "quality_score",
    test_size: float = 0.2,
    seed: int = 42,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Run the full preprocessing pipeline.

    Args:
        raw_path: Path to raw CSV data.
        processed_dir: Directory for processed output files.
        scaler_path: Path to save the fitted scaler.
        target_col: Name of the target column.
        test_size: Fraction of data for testing.
        seed: Random seed for splitting.

    Returns:
        Tuple of (X_train, X_test, y_train, y_test) as numpy arrays.
    """
    df = load_raw_data(raw_path)
    X, y = split_features_target(df, target_col)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=seed
    )

    X_train_scaled, X_test_scaled, _ = scale_features(X_train, X_test, scaler_path)

    # Normalize target to [0, 1] for sigmoid output
    y_train = y_train.values / 100.0
    y_test = y_test.values / 100.0

    # Save processed splits
    Path(processed_dir).mkdir(parents=True, exist_ok=True)
    train_df = pd.DataFrame(X_train_scaled, columns=X.columns)
    train_df[target_col] = y_train
    train_df.to_csv(f"{processed_dir}/train.csv", index=False)

    test_df = pd.DataFrame(X_test_scaled, columns=X.columns)
    test_df[target_col] = y_test
    test_df.to_csv(f"{processed_dir}/test.csv", index=False)

    logger.info(f"Preprocessing complete: {len(X_train_scaled)} train, {len(X_test_scaled)} test")
    return X_train_scaled, X_test_scaled, y_train, y_test
