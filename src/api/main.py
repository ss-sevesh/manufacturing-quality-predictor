"""FastAPI prediction service for manufacturing quality scores."""

import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

import numpy as np
import yaml
from fastapi import FastAPI, HTTPException

from src.api.schemas import (
    HealthResponse,
    ModelInfoResponse,
    PredictionRequest,
    PredictionResponse,
)
from src.data.preprocess import load_scaler

logger = logging.getLogger(__name__)

# Global state
_model = None
_scaler = None
_config = None


def _load_config() -> dict:
    config_path = os.getenv("CONFIG_PATH", "configs/config.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model and scaler at startup."""
    global _model, _scaler, _config

    _config = _load_config()
    model_path = os.getenv("MODEL_PATH", _config["training"]["export_path"])
    scaler_path = _config["data"]["scaler_path"]

    keras_path = Path(model_path) / "model.keras"
    if keras_path.exists():
        from tensorflow import keras
        _model = keras.models.load_model(str(keras_path))
        logger.info(f"Model loaded from {keras_path}")

    if Path(scaler_path).exists():
        _scaler = load_scaler(scaler_path)
        logger.info(f"Scaler loaded from {scaler_path}")

    yield

    _model = None
    _scaler = None


app = FastAPI(
    title="Manufacturing Quality Predictor",
    description="Predict manufacturing quality scores from process sensor data",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Liveness and readiness check."""
    return HealthResponse(status="healthy", model_loaded=_model is not None)


@app.get("/model/info", response_model=ModelInfoResponse)
async def model_info() -> ModelInfoResponse:
    """Return loaded model metadata."""
    if _model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    return ModelInfoResponse(
        model_name="quality_predictor_mlp",
        input_features=_config["model"]["architecture"]["input_dim"],
        architecture=str(_config["model"]["architecture"]["hidden_layers"]),
        version="0.1.0",
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest) -> PredictionResponse:
    """Predict quality score from manufacturing sensor data.

    Args:
        request: Sensor readings for a single manufactured part.

    Returns:
        Predicted quality score, confidence, and pass/fail status.
    """
    if _model is None or _scaler is None:
        raise HTTPException(status_code=503, detail="Model or scaler not loaded")

    features = np.array([[
        request.temperature,
        request.pressure,
        request.vibration,
        request.humidity,
        request.speed,
        request.thickness,
        request.power_consumption,
        request.tool_wear,
        request.coolant_flow,
        request.ambient_temp,
        request.cycle_time,
        request.material_hardness,
        request.spindle_load,
        request.feed_rate,
        request.surface_roughness,
    ]])

    features_scaled = _scaler.transform(features)
    prediction = _model.predict(features_scaled, verbose=0)

    quality_score = float(prediction[0][0]) * 100
    quality_score = max(0, min(100, quality_score))

    threshold = _config["api"]["quality_threshold"]
    status = "pass" if quality_score >= threshold else "fail"

    # Confidence based on distance from decision boundary
    distance = abs(quality_score - threshold) / 100
    confidence = min(1.0, 0.5 + distance)

    return PredictionResponse(
        quality_score=round(quality_score, 2),
        confidence=round(confidence, 3),
        status=status,
    )
