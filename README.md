# Manufacturing Quality Score Predictor

An end-to-end machine learning system that predicts quality scores (0–100) for manufactured parts from 15 real-time process sensor readings. A Multi-Layer Perceptron (MLP) trained with TensorFlow/Keras powers the predictions; a FastAPI backend serves them; a React dashboard visualises them.

---

## How It Works

```
Sensor Data (15 features)
        │
        ▼
 Data Validation          ← schema, null, and range checks
        │
        ▼
 StandardScaler           ← fit on train split, reused at inference
        │
        ▼
 MLP Regressor            ← Dense(128→64→32) + Sigmoid output
        │
        ▼
 Quality Score (0–100)    ← pass if ≥ 70, fail otherwise
        │
        ▼
 FastAPI  /predict        ← JSON request → {score, confidence, status}
        │
        ▼
 React Dashboard          ← live gauges, history, performance metrics
```

The quality score is a nonlinear function of temperature, pressure, vibration, tool wear, coolant flow, humidity, speed, surface roughness, material hardness, and cycle time — with Gaussian noise to simulate measurement variability. Five additional features (thickness, power consumption, ambient temperature, spindle load, feed rate) are included as realistic process parameters that the model must learn to de-weight.

---

## Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Deep Learning | TensorFlow + Keras | 2.19.0 / 3.9.2 |
| Preprocessing | scikit-learn | 1.6.1 |
| Data Manipulation | pandas + numpy | 2.1.4 / 1.26.4 |
| Experiment Tracking | MLflow | 2.21.0 |
| Explainability | SHAP | 0.46.0 |
| API Server | FastAPI + Uvicorn | 0.115.12 / 0.34.0 |
| Frontend | React + Vite + Tailwind | 19 / 8 / 4 |
| Testing | pytest + httpx | 8.3.5 / 0.28.1 |
| Config | PyYAML + python-dotenv | 6.0.2 / 1.1.0 |
| Containerisation | Docker + Docker Compose | — |

---

## Project Structure

```
manufacturing-quality-predictor/
├── src/
│   ├── data/
│   │   ├── generate_data.py     # synthetic dataset generator
│   │   ├── preprocess.py        # scaling, splitting, scaler serialisation
│   │   └── validate.py          # schema / null / range checks
│   ├── models/
│   │   ├── mlp_model.py         # Keras MLP builder + callbacks
│   │   ├── train.py             # training loop + MLflow tracking
│   │   └── evaluate.py          # metrics (MAE, RMSE, R², MAPE) + SHAP
│   ├── visualization/
│   │   └── plots.py             # distribution, correlation, residual plots
│   └── api/
│       ├── main.py              # FastAPI app with /predict, /health, /model/info
│       └── schemas.py           # Pydantic request / response models
├── frontend/                    # React SPA (Vite + Tailwind)
│   └── src/
│       ├── pages/               # Dashboard, Predict, History, Performance, Monitoring
│       ├── components/          # KpiCard, ScoreBadge, Navbar, Sidebar
│       ├── hooks/               # React Query hooks for API calls
│       └── utils/               # helpers, localStorage history
├── configs/
│   └── config.yaml              # all hyperparameters and paths
├── data/
│   ├── raw/                     # generated CSV
│   └── processed/               # scaled splits + scaler.pkl
├── models/
│   ├── final/                   # model.keras (production)
│   └── checkpoints/             # best_model.keras (best val_loss)
├── notebooks/
│   └── 01_eda.ipynb             # exploratory data analysis
├── tests/
│   ├── test_data.py             # data generation + validation tests
│   ├── test_model.py            # MLP build + metrics tests
│   └── test_api.py              # FastAPI endpoint tests
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml       # API + MLflow server
├── docs/
│   └── architecture.md          # detailed component architecture
├── mlruns/                      # MLflow experiment artifacts
├── logs/                        # application logs
├── requirements.txt
└── .env.example
```

---

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+ (for the React frontend)
- Docker (optional)

### 1 — Python Environment

```bash
git clone <repo-url>
cd manufacturing-quality-predictor

python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env
```

### 2 — Generate Training Data

```bash
python -m src.data.generate_data
# → data/raw/manufacturing_data.csv  (10 000 rows, 16 columns)
```

### 3 — Train the Model

```bash
python -m src.models.train
# → models/final/model.keras
# → models/checkpoints/best_model.keras
# → mlruns/  (MLflow artifacts)
```

Training is fully config-driven (`configs/config.yaml`). Every run is logged to MLflow — launch the UI to inspect:

```bash
mlflow ui --backend-store-uri mlruns
# open http://localhost:5000
```

### 4 — Start the API

```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

Interactive API docs: `http://localhost:8000/docs`

### 5 — Start the React Dashboard

```bash
cd frontend
npm install
npm run dev
# open http://localhost:5173
```

---

## API Reference

### `POST /predict`

Send 15 sensor readings, receive a predicted quality score.

**Request**

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
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
    "surface_roughness": 1.2
  }'
```

**Response**

```json
{
  "quality_score": 87.3,
  "confidence": 0.924,
  "status": "pass"
}
```

`status` is `"pass"` when `quality_score ≥ 70` (configurable via `api.quality_threshold` in `config.yaml`).

### `GET /health`

```json
{ "status": "healthy", "model_loaded": true }
```

### `GET /metrics`

Returns saved training metrics including MAE, RMSE, R², MAPE, loss history, and a scatter sample of actual vs predicted values.

```json
{
  "mae": 1.804,
  "rmse": 2.259,
  "r2": 0.4835,
  "mape": 2.35,
  "training_epochs": 45,
  "train_samples": 8000,
  "test_samples": 2000
}
```

### `GET /model/info`

```json
{
  "model_name": "quality_predictor_mlp",
  "input_features": 15,
  "architecture": "[128, 64, 32]",
  "version": "0.1.0"
}
```

---

## Input Features

| Feature | Unit | Range |
|---|---|---|
| temperature | °C | 100 – 300 |
| pressure | bar | 20 – 80 |
| vibration | mm/s | 0 – 1.0 |
| humidity | % | 10 – 100 |
| speed | RPM | 500 – 2000 |
| thickness | mm | 0.5 – 5.0 |
| power_consumption | W | 200 – 500 |
| tool_wear | ratio (0–1) | 0 – 1.0 |
| coolant_flow | L/min | 0 – 20 |
| ambient_temp | °C | 10 – 45 |
| cycle_time | s | 20 – 80 |
| material_hardness | HRC | 30 – 80 |
| spindle_load | % | 20 – 100 |
| feed_rate | mm/rev | 0.05 – 0.5 |
| surface_roughness | μm | 0 – 20 |

---

## Configuration

All hyperparameters, paths, and runtime options live in `configs/config.yaml`. Key sections:

```yaml
data:
  num_samples: 10000
  test_size: 0.2
  random_seed: 42

model:
  architecture:
    hidden_layers: [128, 64, 32]
    dropout_rate: 0.3
    output_activation: sigmoid
  hyperparameters:
    learning_rate: 0.001
    batch_size: 64
    epochs: 100

api:
  quality_threshold: 70.0   # score below this → status: fail
```

---

## Running Tests

```bash
pytest tests/ -v
```

Test files are scaffolded in `tests/` (test_data.py, test_model.py, test_api.py). Target: ≥ 80% coverage.

---

## Docker

```bash
cd docker
docker-compose up --build
```

Starts two services:

| Service | Port | Description |
|---|---|---|
| `quality-predictor-api` | 8000 | FastAPI prediction server |
| `quality-predictor-mlflow` | 5000 | MLflow tracking UI |

The API container expects a trained model to exist at `models/final/model.keras`. Run training locally first and the `models/` volume is mounted into the container.

---

## Dashboard Pages

| Page | Description |
|---|---|
| **Dashboard** | Average quality score gauge, total predictions, defect rate (API `status: fail`) |
| **Predict** | Form with all 15 sensor inputs; live score result with confidence |
| **History** | Paginated log of all predictions, score-range filter, CSV export |
| **Performance** | Model metrics (RMSE, MAE, R²), actual vs predicted scatter, SHAP bar chart, training loss curve |
| **Monitoring** | Live quality trend line updated every 5 s, alert panel for below-threshold predictions |

Prediction history is persisted in browser `localStorage` so it survives page refreshes.

---

## MLflow Experiment Tracking

Every training run automatically logs:

- **Parameters**: hidden layers, dropout, learning rate, batch size, epochs, sample counts
- **Metrics per epoch**: `train_loss`, `val_loss`
- **Test metrics**: `test_loss`, `test_mae`, `test_mse`
- **Artifact**: full Keras model

---

## License

MIT
