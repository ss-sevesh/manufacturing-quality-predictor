"""Visualization utilities for EDA and model analysis.

Provides reusable plotting functions for data exploration,
training diagnostics, and model evaluation.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

logger = logging.getLogger(__name__)


def plot_feature_distributions(
    df: pd.DataFrame, output_path: Optional[str] = None
) -> plt.Figure:
    """Plot histograms for all numeric features.

    Args:
        df: Input DataFrame.
        output_path: Optional path to save the figure.

    Returns:
        Matplotlib Figure object.
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    n_cols = 4
    n_rows = (len(numeric_cols) + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 3 * n_rows))
    axes = axes.flatten()

    for i, col in enumerate(numeric_cols):
        axes[i].hist(df[col], bins=50, edgecolor="black", alpha=0.7)
        axes[i].set_title(col)

    for i in range(len(numeric_cols), len(axes)):
        axes[i].set_visible(False)

    fig.suptitle("Feature Distributions", fontsize=14)
    fig.tight_layout()

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
        logger.info(f"Saved distribution plot to {output_path}")

    return fig


def plot_correlation_matrix(
    df: pd.DataFrame, output_path: Optional[str] = None
) -> plt.Figure:
    """Plot a correlation heatmap.

    Args:
        df: Input DataFrame.
        output_path: Optional path to save the figure.

    Returns:
        Matplotlib Figure object.
    """
    fig, ax = plt.subplots(figsize=(12, 10))
    corr = df.select_dtypes(include=[np.number]).corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
    ax.set_title("Feature Correlation Matrix")
    fig.tight_layout()

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=150, bbox_inches="tight")

    return fig


def plot_training_history(
    history: Dict[str, List[float]], output_path: Optional[str] = None
) -> plt.Figure:
    """Plot training and validation loss curves.

    Args:
        history: Keras History.history dictionary.
        output_path: Optional path to save the figure.

    Returns:
        Matplotlib Figure object.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].plot(history["loss"], label="Train Loss")
    axes[0].plot(history["val_loss"], label="Val Loss")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Loss (MSE)")
    axes[0].set_title("Training vs Validation Loss")
    axes[0].legend()

    if "mae" in history:
        axes[1].plot(history["mae"], label="Train MAE")
        axes[1].plot(history["val_mae"], label="Val MAE")
        axes[1].set_xlabel("Epoch")
        axes[1].set_ylabel("MAE")
        axes[1].set_title("Training vs Validation MAE")
        axes[1].legend()

    fig.tight_layout()

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=150, bbox_inches="tight")

    return fig


def plot_predictions_vs_actual(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    output_path: Optional[str] = None,
) -> plt.Figure:
    """Plot predicted vs actual scatter with diagonal reference.

    Args:
        y_true: Ground truth values.
        y_pred: Model predictions.
        output_path: Optional path to save the figure.

    Returns:
        Matplotlib Figure object.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Scatter plot
    axes[0].scatter(y_true, y_pred, alpha=0.3, s=10)
    axes[0].plot([0, 100], [0, 100], "r--", linewidth=2)
    axes[0].set_xlabel("Actual Quality Score")
    axes[0].set_ylabel("Predicted Quality Score")
    axes[0].set_title("Predicted vs Actual")

    # Residuals
    residuals = y_pred - y_true
    axes[1].hist(residuals, bins=50, edgecolor="black", alpha=0.7)
    axes[1].axvline(x=0, color="r", linestyle="--")
    axes[1].set_xlabel("Residual (Predicted - Actual)")
    axes[1].set_ylabel("Count")
    axes[1].set_title("Residual Distribution")

    fig.tight_layout()

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=150, bbox_inches="tight")

    return fig
