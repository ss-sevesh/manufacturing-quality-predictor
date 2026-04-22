"""Model evaluation and explainability.

Computes regression metrics, generates diagnostic plots,
and runs SHAP analysis for feature importance.
"""

import logging
from typing import Dict

import numpy as np
import shap
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from tensorflow import keras

logger = logging.getLogger(__name__)


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """Compute regression evaluation metrics.

    Predictions and targets are assumed to be in [0, 1] scale (sigmoid output).
    Metrics are computed on the original 0-100 scale for interpretability.

    Args:
        y_true: Ground truth values in [0, 1].
        y_pred: Predicted values in [0, 1].

    Returns:
        Dictionary with MAE, RMSE, R2, and MAPE on the 0-100 scale.
    """
    y_true_100 = y_true * 100
    y_pred_100 = y_pred.flatten() * 100

    mae = mean_absolute_error(y_true_100, y_pred_100)
    rmse = np.sqrt(mean_squared_error(y_true_100, y_pred_100))
    r2 = r2_score(y_true_100, y_pred_100)

    # MAPE with epsilon to avoid division by zero
    mape = np.mean(np.abs((y_true_100 - y_pred_100) / (y_true_100 + 1e-8))) * 100

    metrics = {"mae": mae, "rmse": rmse, "r2": r2, "mape": mape}
    logger.info(f"Evaluation metrics: {metrics}")
    return metrics


def evaluate_model(
    model: keras.Model, X_test: np.ndarray, y_test: np.ndarray
) -> Dict[str, float]:
    """Evaluate a trained model on test data.

    Args:
        model: Trained Keras model.
        X_test: Scaled test features.
        y_test: Test targets in [0, 1].

    Returns:
        Dictionary of evaluation metrics.
    """
    y_pred = model.predict(X_test, verbose=0)
    return compute_metrics(y_test, y_pred)


def shap_analysis(
    model: keras.Model,
    X_train: np.ndarray,
    X_test: np.ndarray,
    feature_names: list,
    num_background: int = 100,
) -> shap.Explanation:
    """Run SHAP analysis for feature importance.

    Uses DeepExplainer with a background sample from the training set.

    Args:
        model: Trained Keras model.
        X_train: Scaled training features (for background distribution).
        X_test: Scaled test features to explain.
        feature_names: List of feature names.
        num_background: Number of background samples for SHAP.

    Returns:
        SHAP Explanation object.
    """
    background = X_train[:num_background]
    explainer = shap.DeepExplainer(model, background)
    shap_values = explainer.shap_values(X_test[:200])

    logger.info("SHAP analysis complete")
    return shap.Explanation(
        values=shap_values[0] if isinstance(shap_values, list) else shap_values,
        data=X_test[:200],
        feature_names=feature_names,
    )
