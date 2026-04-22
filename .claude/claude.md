# Manufacturing Quality Score Prediction

## Project Overview
An end-to-end ML system that predicts manufacturing quality scores using a Multi-Layer Perceptron (MLP) deep learning model. The system ingests sensor and process data from manufacturing lines, preprocesses it, trains an MLP regressor, and serves predictions via a FastAPI REST API.

**Goal:** Predict a continuous quality score (0-100) for manufactured parts based on process parameters, enabling proactive quality control and reducing defect rates.

## Tech Stack

| Layer              | Technology                        |
|--------------------|-----------------------------------|
| Deep Learning      | TensorFlow / Keras                |
| Hyperparameter Tuning | Keras Tuner                    |
| Classical ML       | scikit-learn (preprocessing)      |
| Data Validation    | Great Expectations                |
| Experiment Tracking| MLflow                            |
| Explainability     | SHAP                              |
| API                | FastAPI + Uvicorn                 |
| Dashboard          | Streamlit                         |
| Model Export       | ONNX (tf2onnx)                    |
| Visualization      | Matplotlib, Seaborn, Plotly       |
| Testing            | pytest                            |
| Config             | PyYAML + python-dotenv            |
| Containerization   | Docker + Docker Compose           |

## Coding Conventions
- **Naming:** `snake_case` for functions, variables, modules; `PascalCase` for classes
- **Type hints:** Required on all function signatures
- **Docstrings:** Google-style docstrings on every public function and class
- **Imports:** stdlib -> third-party -> local, separated by blank lines
- **Max line length:** 100 characters
- **Logging:** Use Python `logging` module, never `print()` in production code

## Folder Structure
```
src/data/          - Data generation, preprocessing, validation
src/models/        - MLP architecture, training loop, evaluation metrics
src/visualization/ - Plotting utilities for EDA and model analysis
src/api/           - FastAPI prediction service and request/response schemas
configs/           - YAML configuration files
data/raw/          - Original unprocessed datasets
data/processed/    - Cleaned, feature-engineered datasets
data/external/     - Third-party reference data
notebooks/         - Jupyter notebooks for exploration
tests/             - pytest unit and integration tests
logs/              - Application and training logs
mlruns/            - MLflow experiment artifacts
docker/            - Container definitions
docs/              - Architecture and design documentation
```

## Key Rules
1. **Always use virtual env:** Never install packages globally. Activate `venv` before any work.
2. **Log everything to MLflow:** Every training run, hyperparameter set, metric, and artifact must be tracked in MLflow.
3. **Write tests for every module:** No module ships without corresponding tests in `tests/`. Minimum 80% coverage target.
4. **Validate data before training:** Run Great Expectations suites before any model training.
5. **Config-driven:** All hyperparameters and paths live in `configs/config.yaml`, never hardcoded.
6. **Reproducibility:** Set random seeds everywhere. Log the full config with each MLflow run.
