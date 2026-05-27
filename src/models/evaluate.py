"""Model evaluation metrics."""

import logging
from typing import Dict

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from tensorflow import keras

logger = logging.getLogger(__name__)


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """Compute regression metrics on the 0-100 scale.

    Args:
        y_true: Ground truth values in [0, 1].
        y_pred: Predicted values in [0, 1].

    Returns:
        Dictionary with MAE, RMSE, R2, and MAPE.
    """
    y_true_100 = y_true * 100
    y_pred_100 = y_pred.flatten() * 100

    mae = mean_absolute_error(y_true_100, y_pred_100)
    rmse = np.sqrt(mean_squared_error(y_true_100, y_pred_100))
    r2 = r2_score(y_true_100, y_pred_100)
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
