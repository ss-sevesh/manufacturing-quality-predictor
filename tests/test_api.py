"""Tests for the FastAPI prediction service."""

import pytest
from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)

VALID_PAYLOAD = {
    "temperature": 185.0,
    "pressure": 45.2,
    "vibration": 0.03,
    "humidity": 62.0,
    "speed": 1200,
    "thickness": 2.5,
    "power_consumption": 340.0,
    "tool_wear": 0.15,
    "coolant_flow": 8.5,
    "ambient_temp": 24.0,
    "cycle_time": 45.0,
    "material_hardness": 58.0,
    "spindle_load": 72.0,
    "feed_rate": 0.25,
    "surface_roughness": 1.2,
}


class TestHealthEndpoint:
    def test_health_returns_200(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "model_loaded" in data


class TestModelInfoEndpoint:
    def test_model_info_without_model(self):
        response = client.get("/model/info")
        # 503 when model is not loaded
        assert response.status_code == 503


class TestPredictEndpoint:
    def test_predict_without_model_returns_503(self):
        response = client.post("/predict", json=VALID_PAYLOAD)
        assert response.status_code == 503

    def test_predict_invalid_payload(self):
        response = client.post("/predict", json={"temperature": 185.0})
        assert response.status_code == 422

    def test_predict_out_of_range_values(self):
        bad_payload = VALID_PAYLOAD.copy()
        bad_payload["temperature"] = 999  # exceeds max
        response = client.post("/predict", json=bad_payload)
        assert response.status_code == 422
