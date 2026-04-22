# Manufacturing Quality Score Prediction

Predict manufacturing quality scores (0-100) from process sensor data using a Multi-Layer Perceptron deep learning model. Enables proactive quality control by identifying parts likely to fall below quality thresholds before they reach inspection.

## Architecture

```
+------------------+     +------------------+     +------------------+
|   Raw Sensor     |     |  Preprocessing   |     |   MLP Model      |
|   Data (CSV)     +---->+  Pipeline        +---->+   (TensorFlow)   |
|                  |     |  (scikit-learn)  |     |                  |
+------------------+     +------------------+     +--------+---------+
                                                           |
                              +----------------------------+
                              |
                    +---------v---------+     +------------------+
                    |   MLflow          |     |   FastAPI        |
                    |   Tracking        |     |   REST API       |
                    +-------------------+     +--------+---------+
                                                       |
                                              +--------v---------+
                                              |   Streamlit      |
                                              |   Dashboard      |
                                              +------------------+
```

### Data Flow

```
generate_data.py --> data/raw/manufacturing_data.csv
                          |
                     validate.py (Great Expectations)
                          |
                     preprocess.py --> data/processed/train.csv, test.csv
                          |
                     train.py --> mlruns/ (MLflow artifacts)
                          |
                     evaluate.py --> metrics, plots, SHAP analysis
                          |
                     main.py (FastAPI) --> /predict endpoint
```

## Tech Stack

| Component            | Technology           | Version  |
|----------------------|----------------------|----------|
| Deep Learning        | TensorFlow + Keras   | 2.19.0   |
| Hyperparameter Tuning| Keras Tuner          | 1.4.7    |
| Preprocessing        | scikit-learn         | 1.6.1    |
| Data Manipulation    | pandas + numpy       | 2.2.3    |
| Experiment Tracking  | MLflow               | 2.21.0   |
| Explainability       | SHAP                 | 0.46.0   |
| API Server           | FastAPI + Uvicorn    | 0.115.12 |
| Dashboard            | Streamlit            | 1.43.2   |
| Data Validation      | Great Expectations   | 1.3.12   |
| Visualization        | Matplotlib, Seaborn, Plotly | --  |
| Testing              | pytest               | 8.3.5    |
| Containerization     | Docker               | --       |

## Setup

### Prerequisites
- Python 3.10+
- pip
- Docker (optional, for containerized deployment)

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd manufacturing-quality-predictor

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
```

### Generate Data

```bash
python -m src.data.generate_data
```

### Train Model

```bash
python -m src.models.train
```

### Run API

```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

### Run Tests

```bash
pytest tests/ -v
```

### Docker

```bash
cd docker
docker-compose up --build
```

## Usage

### Prediction Request

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

### Response

```json
{
  "quality_score": 87.3,
  "confidence": 0.92,
  "status": "pass"
}
```

## Project Structure

```
manufacturing-quality-predictor/
├── src/                  # Source code modules
│   ├── data/             # Data generation, preprocessing, validation
│   ├── models/           # MLP architecture, training, evaluation
│   ├── visualization/    # Plotting utilities
│   └── api/              # FastAPI prediction service
├── configs/              # YAML configuration
├── data/                 # Raw, processed, and external data
├── notebooks/            # Jupyter EDA notebooks
├── tests/                # Unit and integration tests
├── docker/               # Container definitions
├── docs/                 # Architecture documentation
├── logs/                 # Application logs
└── mlruns/               # MLflow experiment tracking
```

## License

MIT
