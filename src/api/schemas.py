"""Pydantic schemas for API request/response validation."""

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """Input schema for manufacturing quality prediction."""

    temperature: float = Field(..., ge=100, le=300, description="Process temperature (C)")
    pressure: float = Field(..., ge=20, le=80, description="Process pressure (bar)")
    vibration: float = Field(..., ge=0, le=1.0, description="Vibration level (mm/s)")
    humidity: float = Field(..., ge=10, le=100, description="Relative humidity (%)")
    speed: float = Field(..., ge=500, le=2000, description="Spindle speed (RPM)")
    thickness: float = Field(..., ge=0.5, le=5.0, description="Material thickness (mm)")
    power_consumption: float = Field(..., ge=200, le=500, description="Power consumption (W)")
    tool_wear: float = Field(..., ge=0, le=1.0, description="Tool wear ratio (0-1)")
    coolant_flow: float = Field(..., ge=0, le=20, description="Coolant flow rate (L/min)")
    ambient_temp: float = Field(..., ge=10, le=45, description="Ambient temperature (C)")
    cycle_time: float = Field(..., ge=20, le=80, description="Cycle time (seconds)")
    material_hardness: float = Field(..., ge=30, le=80, description="Material hardness (HRC)")
    spindle_load: float = Field(..., ge=20, le=100, description="Spindle load (%)")
    feed_rate: float = Field(..., ge=0.05, le=0.5, description="Feed rate (mm/rev)")
    surface_roughness: float = Field(..., ge=0, le=20, description="Surface roughness (um)")

    class Config:
        json_schema_extra = {
            "example": {
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
        }


class PredictionResponse(BaseModel):
    """Output schema for quality score prediction."""

    quality_score: float = Field(..., description="Predicted quality score (0-100)")
    confidence: float = Field(..., description="Model confidence (0-1)")
    status: str = Field(..., description="Quality status: pass or fail")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    model_loaded: bool


class ModelInfoResponse(BaseModel):
    """Model metadata response."""

    model_name: str
    input_features: int
    architecture: str
    version: str
