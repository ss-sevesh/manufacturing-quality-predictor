# Progress Tracker

## Completed

- [x] Project structure created
- [x] Configuration files set up (config.yaml, .env.example, .gitignore)
- [x] Requirements defined with pinned versions
- [x] Docker configuration written
- [x] Documentation scaffolding in place (README, architecture, TASKS, CHANGELOG)
- [x] Source module scaffolding with __init__.py files
- [x] Synthetic data generation (generate_data.py) — 10,000 samples, 15 features
- [x] Data validation (validate.py) — schema, null, and range checks
- [x] Data preprocessing pipeline (preprocess.py) — StandardScaler, train/test split, target normalization
- [x] MLP model architecture (mlp_model.py) — Keras Sequential [128→64→32], dropout, callbacks
- [x] Training loop with MLflow integration (train.py) — EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
- [x] Model trained and saved (models/final/model.keras) — 45 epochs, MAE 1.80, RMSE 2.26, MAPE 2.35%
- [x] Evaluation metrics (evaluate.py) — MAE, RMSE, R², MAPE on 0-100 scale
- [x] FastAPI prediction service (main.py) — /predict, /health, /model-info, /metrics endpoints
- [x] Pydantic request/response schemas (schemas.py)
- [x] React/Vite frontend — Dashboard, Predict, History, Performance pages
- [x] API tested and verified (prediction returning correct scores)
- [x] MLflow experiment tracking running

## In Progress

- [ ] EDA notebook (01_eda.ipynb)
- [ ] Unit tests (test_api.py, test_data.py, test_model.py) — scaffolded, not filled

## Blocked

_Nothing currently blocked._

## Notes

- Using TensorFlow/Keras for MLP implementation
- Quality score is a continuous target (0-100) — regression problem
- Synthetic data simulates 15 manufacturing process features
- Model metrics: MAE=1.80, RMSE=2.26, R²=0.48, MAPE=2.35% (acceptable for demo/basic project)
- R² is lower due to narrow quality score distribution in synthetic data (most samples cluster ~70-80)
- API running on http://localhost:8000 | Frontend on http://localhost:5173
