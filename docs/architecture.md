# System Architecture

## Overview

The Manufacturing Quality Score Prediction system is a supervised regression pipeline that predicts a continuous quality score (0–100) for manufactured parts based on 15 process sensor features. The system consists of four main layers: data, model, serving, and frontend.

## Component Architecture

### 1. Data Layer

**Data Generation (`src/data/generate_data.py`)**
- Produces synthetic manufacturing sensor data simulating realistic correlations between process parameters and quality outcomes
- Features include temperature, pressure, vibration, humidity, speed, thickness, power consumption, tool wear, coolant flow, ambient temperature, cycle time, material hardness, spindle load, feed rate, and surface roughness
- Quality score is generated as a nonlinear function of a subset of these features with added Gaussian noise

**Data Validation (`src/data/validate.py`)**
- Enforces data contracts using pandas: all required columns present, no null values, all values within physical bounds
- Called automatically inside `preprocess_pipeline()` before any transformation or splitting

**Preprocessing (`src/data/preprocess.py`)**
- StandardScaler normalization fitted on training data, applied to both splits
- Random train/test split (no stratification) with configurable `test_size`
- Scaler serialized to `data/processed/scaler.pkl` for consistent inference-time transforms
- Target normalized to [0, 1] to match sigmoid output layer

### 2. Model Layer

**MLP Architecture (`src/models/mlp_model.py`)**
- Input: 15 normalized features
- Hidden layers: 128 → 64 → 32 neurons with ReLU activation and dropout (0.3)
- Output: single neuron with sigmoid activation, scaled to 0–100 at inference
- Loss: Mean Squared Error; Optimizer: Adam with learning rate scheduling

**Training (`src/models/train.py`)**
- Config-driven hyperparameters loaded from `configs/config.yaml`
- Global TensorFlow random seed set for reproducibility
- Callbacks: EarlyStopping, ReduceLROnPlateau, ModelCheckpoint (saves best val_loss checkpoint)
- Full MLflow integration: logs parameters, per-epoch loss metrics, and final model artifact

**Evaluation (`src/models/evaluate.py`)**
- Metrics computed on original 0–100 scale: MAE, RMSE, R-squared, MAPE
- SHAP DeepExplainer for feature importance analysis

### 3. Serving Layer

**FastAPI Service (`src/api/main.py`)**
- `POST /predict` — accepts sensor readings, returns quality score, confidence, and pass/fail status
- `GET /health` — liveness and readiness check
- `GET /model/info` — returns loaded model metadata
- CORS enabled for all origins (configurable for production)
- Request/response validation via Pydantic schemas (`src/api/schemas.py`)

**ONNX Export (optional)**
- Dependencies (`onnx`, `tf2onnx`) are included in requirements for users who want to export the trained Keras model to ONNX for optimized inference
- The API currently loads the `.keras` model directly; ONNX export is a planned enhancement

### 4. Frontend Layer

**React SPA (`frontend/`)**
- Built with React 19, Vite, and Tailwind CSS
- Pages: Dashboard (KPI overview + gauges), Predict (sensor input form), History (paginated prediction log + CSV export), Performance (model diagnostics charts), Monitoring (live quality trend + alerts)
- Prediction history is persisted in `localStorage`
- Communicates with the FastAPI backend at `http://localhost:8000`

**MLflow Tracking**
- All experiments, parameters, metrics, and artifacts logged
- Model registry for version management and stage transitions

## Data Flow

```
[Sensors / generate_data.py]
        |
        v
  data/raw/manufacturing_data.csv
        |
        v
  validate.py (schema, null, range checks)
        |
        v
  preprocess.py (scaling, train/test split)
        |
        v
  data/processed/{train.csv, test.csv, scaler.pkl}
        |
        v
  train.py (MLP training + MLflow logging)
        |
        v
  models/final/model.keras
  models/checkpoints/best_model.keras
        |
        v
  main.py (FastAPI loads model, serves /predict)
        |
        v
  React frontend (Dashboard, Predict, History, Performance, Monitoring)
```

## Model Design

The MLP regressor maps 15 manufacturing process features to a single quality score:

```
Input (15) --> Dense(128, ReLU) --> Dropout(0.3)
          --> Dense(64, ReLU)  --> Dropout(0.3)
          --> Dense(32, ReLU)  --> Dropout(0.3)
          --> Dense(1, Sigmoid) --> Scale to [0, 100]
```

Sigmoid output ensures bounded predictions in [0, 1] (scaled to 0–100 at the API layer). The model is trained with MSE loss and evaluated with MAE as the primary business metric (directly interpretable as average point error on the 0–100 scale).

## Deployment

The API service runs in a Docker container behind Uvicorn with 4 workers. Docker Compose orchestrates the API service and an MLflow tracking server. The containerized API loads the `.keras` model at startup and serves predictions.
