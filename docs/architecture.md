# System Architecture

## Overview

The Manufacturing Quality Score Prediction system is a supervised regression pipeline that predicts a continuous quality score (0-100) for manufactured parts based on 15 process sensor features. The system consists of four main layers: data, model, serving, and monitoring.

## Component Architecture

### 1. Data Layer

**Data Generation (`src/data/generate_data.py`)**
- Produces synthetic manufacturing sensor data simulating realistic correlations between process parameters and quality outcomes
- Features include temperature, pressure, vibration, humidity, speed, thickness, power consumption, tool wear, coolant flow, ambient temperature, cycle time, material hardness, spindle load, feed rate, and surface roughness
- Quality score is generated as a nonlinear function of these features with added noise

**Data Validation (`src/data/validate.py`)**
- Uses Great Expectations to enforce data contracts: no nulls, correct dtypes, value ranges within physical limits
- Runs before every training pipeline execution to catch upstream data issues early

**Preprocessing (`src/data/preprocess.py`)**
- StandardScaler normalization on all continuous features
- Train/test split with stratification on quality score bins
- Scaler serialization for inference-time consistency

### 2. Model Layer

**MLP Architecture (`src/models/mlp_model.py`)**
- Input: 15 normalized features
- Hidden layers: 128 -> 64 -> 32 neurons with ReLU activation and dropout (0.3)
- Output: single neuron with sigmoid activation, scaled to 0-100
- Loss: Mean Squared Error
- Optimizer: Adam with learning rate scheduling

**Training (`src/models/train.py`)**
- Config-driven hyperparameters loaded from `configs/config.yaml`
- Callbacks: EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
- Full MLflow integration: logs parameters, metrics per epoch, final model artifact, training plots

**Evaluation (`src/models/evaluate.py`)**
- Metrics: MAE, RMSE, R-squared, MAPE
- Residual analysis and prediction distribution plots
- SHAP feature importance analysis

### 3. Serving Layer

**FastAPI Service (`src/api/main.py`)**
- `POST /predict` - accepts sensor readings, returns quality score and pass/fail status
- `GET /health` - liveness check
- `GET /model/info` - returns loaded model metadata
- Request validation via Pydantic schemas (`src/api/schemas.py`)

**ONNX Export**
- Trained Keras model is exported to ONNX format via tf2onnx for optimized inference
- ONNX runtime used in production for lower latency

### 4. Monitoring Layer

**Streamlit Dashboard**
- Live prediction interface for manual inspection
- Historical prediction distribution
- Feature importance visualization

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
  validate.py (Great Expectations checks)
        |
        v
  preprocess.py (scaling, splitting)
        |
        v
  data/processed/{train.csv, test.csv, scaler.pkl}
        |
        v
  train.py (MLP training + MLflow logging)
        |
        v
  models/final/model.keras + model.onnx
        |
        v
  main.py (FastAPI loads model, serves /predict)
```

## Model Design

The MLP regressor maps 15 manufacturing process features to a single quality score:

```
Input (15) --> Dense(128, ReLU) --> Dropout(0.3)
          --> Dense(64, ReLU)  --> Dropout(0.3)
          --> Dense(32, ReLU)  --> Dropout(0.3)
          --> Dense(1, Sigmoid) --> Scale to [0, 100]
```

Sigmoid output ensures bounded predictions. The model is trained with MSE loss and evaluated with MAE as the primary business metric (directly interpretable as average point error on the 0-100 scale).

## Deployment

The API service runs in a Docker container behind Uvicorn with 4 workers. Docker Compose orchestrates the API and MLflow server. The containerized service loads the ONNX model at startup and serves predictions with sub-100ms latency per request.
