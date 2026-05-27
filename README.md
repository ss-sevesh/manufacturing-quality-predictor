# Manufacturing Quality Score Predictor

An end-to-end ML system that predicts quality scores (0–100) for manufactured parts from 15 real-time process sensor readings. A Multi-Layer Perceptron (MLP) trained with TensorFlow/Keras powers the predictions; a FastAPI backend serves them; a React dashboard visualises them.

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

---

## Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Deep Learning | TensorFlow + Keras | 2.19.0 / 3.9.2 |
| Preprocessing | scikit-learn | 1.6.1 |
| Data Manipulation | pandas + numpy | 2.1.4 / 1.26.4 |
| Experiment Tracking | MLflow | 2.21.0 |
| Visualization | Matplotlib + Seaborn | 3.10.1 / 0.13.2 |
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
│   │   └── evaluate.py          # metrics (MAE, RMSE, R², MAPE)
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
│   ├── raw/                     # generated CSV (created at runtime)
│   └── processed/               # scaled splits + scaler.pkl (created at runtime)
├── models/
│   ├── final/                   # model.keras (created after training)
│   └── checkpoints/             # best_model.keras (best val_loss)
├── notebooks/
│   └── 01_eda.ipynb             # exploratory data analysis
├── tests/
│   ├── test_data.py             # data generation + validation tests
│   ├── test_model.py            # MLP build + metrics tests
│   └── test_api.py              # FastAPI endpoint tests
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
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
# → models/final/metrics.json
# → models/checkpoints/best_model.keras
```

All hyperparameters are controlled by `configs/config.yaml` (hidden layers, dropout, learning rate, batch size, epochs). Every run is logged to MLflow:

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

Returns training metrics: MAE, RMSE, R², MAPE, loss history, and actual vs predicted scatter sample.

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

## Hyperparameters

All hyperparameters live in `configs/config.yaml` — no hardcoded values anywhere:

```yaml
model:
  architecture:
    hidden_layers: [128, 64, 32]   # MLP layer sizes
    dropout_rate: 0.3               # regularisation
    activation: relu
    output_activation: sigmoid      # maps output to [0, 1]
  hyperparameters:
    learning_rate: 0.001
    batch_size: 64
    epochs: 100
    optimizer: adam
    loss: mse
  callbacks:
    early_stopping:
      patience: 10                  # stops if val_loss stalls
    reduce_lr:
      factor: 0.5                   # halves LR on plateau
      patience: 5

api:
  quality_threshold: 70.0           # score below this → status: fail
```

---

## Running Tests

```bash
pytest tests/ -v
```

Covers data generation, validation, MLP architecture, metric correctness, and API endpoint contracts.

---

## Docker

```bash
cd docker
docker-compose up --build
```

| Service | Port | Description |
|---|---|---|
| `quality-predictor-api` | 8000 | FastAPI prediction server |
| `quality-predictor-mlflow` | 5000 | MLflow tracking UI |

Train the model locally first — `models/` is mounted as a volume.

---

## MLflow Experiment Tracking

Every training run logs:

- **Parameters**: hidden layers, dropout, learning rate, batch size, epochs, sample counts
- **Metrics per epoch**: `train_loss`, `val_loss`
- **Test metrics**: `test_loss`, `test_mae`, `test_mse`
- **Artifact**: full Keras model

---

## License

MIT
