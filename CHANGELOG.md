# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-05-28

### Added
- Synthetic data generator (src/data/generate_data.py) — 10,000 samples, 15 process features, deterministic quality formula
- Data validation module (src/data/validate.py) — schema, null, and range checks
- Full preprocessing pipeline (src/data/preprocess.py) — StandardScaler, train/test split, target normalization to [0,1]
- MLP model architecture (src/models/mlp_model.py) — Keras Sequential [128→64→32], dropout=0.3, EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
- Training loop with MLflow tracking (src/models/train.py) — logs params, metrics, loss curves, scatter sample, and model artifact
- Evaluation module (src/models/evaluate.py) — MAE, RMSE, R², MAPE on 0-100 scale
- FastAPI prediction service (src/api/main.py) — /predict, /health, /model-info, /metrics endpoints with CORS
- Pydantic schemas (src/api/schemas.py) — PredictionRequest (15 validated fields), PredictionResponse, HealthResponse, ModelInfoResponse
- React/Vite frontend — Dashboard, Predict, History, Performance pages with Tailwind CSS, Recharts, React Query
- metrics.json saved after training for API /metrics endpoint

### Model Performance (baseline)
- MAE: 1.80 | RMSE: 2.26 | R²: 0.48 | MAPE: 2.35%
- Trained for 45 epochs (early stopping), quality threshold: 70.0

## [0.1.0] - 2026-04-21

### Added
- Initial project structure and folder layout
- Configuration files: config.yaml, .env.example, .gitignore
- Requirements with pinned dependency versions
- Docker and docker-compose configuration for API service
- Source module scaffolding: data, models, visualization, api
- Test file scaffolding
- README with setup instructions and architecture overview
- Architecture documentation (docs/architecture.md)
- TASKS.md with phased project checklist
- PROGRESS.md for tracking build status
- Project-level claude.md with coding standards and rules
