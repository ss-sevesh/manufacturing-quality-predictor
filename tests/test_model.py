"""Tests for MLP model architecture and evaluation."""

import numpy as np
import pytest

from src.models.mlp_model import build_mlp
from src.models.evaluate import compute_metrics


class TestBuildMLP:
    def test_model_compiles(self):
        model = build_mlp(input_dim=15, hidden_layers=[64, 32])
        assert model is not None

    def test_output_shape(self):
        model = build_mlp(input_dim=15, hidden_layers=[64, 32])
        dummy_input = np.random.randn(5, 15).astype(np.float32)
        output = model.predict(dummy_input, verbose=0)
        assert output.shape == (5, 1)

    def test_output_bounded_by_sigmoid(self):
        model = build_mlp(input_dim=15, hidden_layers=[64, 32])
        dummy_input = np.random.randn(100, 15).astype(np.float32)
        output = model.predict(dummy_input, verbose=0)
        assert output.min() >= 0
        assert output.max() <= 1

    def test_custom_architecture(self):
        model = build_mlp(
            input_dim=10,
            hidden_layers=[128, 64, 32, 16],
            dropout_rate=0.5,
            learning_rate=0.01,
        )
        # 4 dense + 4 dropout + 1 output = 9 layers
        assert len(model.layers) == 9

    def test_different_activation(self):
        model = build_mlp(
            input_dim=5,
            hidden_layers=[32],
            activation="tanh",
        )
        assert model is not None


class TestMetrics:
    def test_perfect_predictions(self):
        y_true = np.array([0.5, 0.7, 0.9])
        y_pred = np.array([0.5, 0.7, 0.9])
        metrics = compute_metrics(y_true, y_pred)
        assert metrics["mae"] == pytest.approx(0, abs=1e-5)
        assert metrics["rmse"] == pytest.approx(0, abs=1e-5)
        assert metrics["r2"] == pytest.approx(1.0, abs=1e-5)

    def test_metrics_on_known_values(self):
        y_true = np.array([0.5, 0.6, 0.7])
        y_pred = np.array([0.55, 0.65, 0.75])
        metrics = compute_metrics(y_true, y_pred)
        assert metrics["mae"] == pytest.approx(5.0, abs=0.1)
        assert metrics["rmse"] == pytest.approx(5.0, abs=0.1)

    def test_metrics_keys(self):
        y_true = np.array([0.5, 0.7])
        y_pred = np.array([0.6, 0.8])
        metrics = compute_metrics(y_true, y_pred)
        assert set(metrics.keys()) == {"mae", "rmse", "r2", "mape"}
