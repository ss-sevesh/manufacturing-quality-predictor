# Manufacturing Quality Score Prediction

## Project Overview
An end-to-end ML system that predicts manufacturing quality scores using a Multi-Layer Perceptron (MLP). The system ingests sensor and process data, preprocesses it, trains an MLP regressor, and serves predictions via a FastAPI REST API with a React dashboard.

**Goal:** Predict a continuous quality score (0-100) for manufactured parts based on 15 process parameters.

## Tech Stack

| Layer              | Technology                        |
|--------------------|-----------------------------------|
| Deep Learning      | TensorFlow / Keras                |
| Classical ML       | scikit-learn (preprocessing)      |
| Experiment Tracking| MLflow                            |
| Visualization      | Matplotlib, Seaborn               |
| API                | FastAPI + Uvicorn                 |
| Frontend           | React + Vite + Tailwind           |
| Testing            | pytest                            |
| Config             | PyYAML + python-dotenv            |
| Containerization   | Docker + Docker Compose           |

## Coding Conventions
- **Naming:** `snake_case` for functions, variables, modules; `PascalCase` for classes
- **Type hints:** Required on all function signatures
- **Imports:** stdlib -> third-party -> local, separated by blank lines
- **Logging:** Use Python `logging` module, never `print()` in production code

## Folder Structure
```
src/data/          - Data generation, preprocessing, validation
src/models/        - MLP architecture, training loop, evaluation metrics
src/visualization/ - Plotting utilities
src/api/           - FastAPI prediction service and request/response schemas
configs/           - YAML configuration (all hyperparameters and paths)
data/raw/          - Generated CSV dataset (created at runtime)
data/processed/    - Scaled splits and scaler.pkl (created at runtime)
models/            - Trained model artifacts (gitignored, created after training)
notebooks/         - Jupyter notebooks for EDA
tests/             - pytest unit and integration tests
docker/            - Container definitions
```

## Key Rules
1. **Config-driven:** All hyperparameters and paths live in `configs/config.yaml`, never hardcoded.
2. **MLflow tracking:** Every training run logs parameters, metrics, and artifacts.
3. **Reproducibility:** Random seeds set everywhere and logged with each MLflow run.
4. **Tests:** Changes to src/ should have corresponding test coverage in tests/.
