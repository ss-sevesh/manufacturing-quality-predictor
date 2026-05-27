# Project Tasks

## Phase 1: Setup & Data

- [x] Initialize project structure and virtual environment
- [x] Install all dependencies from requirements.txt
- [x] Create synthetic manufacturing dataset (generate_data.py)
- [x] Implement data validation (validate.py) — pandas-based schema/null/range checks
- [x] Build preprocessing pipeline: scaling, train/test split, target normalization (preprocess.py)
- [ ] Run exploratory data analysis notebook (01_eda.ipynb)
- [ ] Write unit tests for data modules

## Phase 2: Model Development

- [x] Define MLP architecture in Keras (mlp_model.py)
- [x] Implement training loop with callbacks and checkpointing (train.py)
- [x] Integrate MLflow experiment tracking into training
- [ ] Run Keras Tuner hyperparameter search
- [x] Train baseline model and log metrics — MAE 1.80, RMSE 2.26, MAPE 2.35%
- [ ] Write unit tests for model modules

## Phase 3: Evaluation & Explainability

- [x] Implement evaluation metrics: MAE, RMSE, R², MAPE (evaluate.py)
- [ ] Generate residual plots and prediction vs actual plots
- [ ] Run SHAP analysis for feature importance
- [ ] Create visualization utilities (plots.py)
- [x] Document model performance in MLflow
- [ ] Write tests for evaluation functions

## Phase 4: API Development

- [x] Build FastAPI prediction endpoint (main.py)
- [x] Define request/response schemas with Pydantic (schemas.py)
- [x] Add health check, model info, and metrics endpoints
- [ ] Write API integration tests (test_api.py)
- [x] Test API with sample prediction requests

## Phase 5: Deployment

- [ ] Export trained model to ONNX format
- [x] Build Docker image for API service (docker/Dockerfile)
- [x] Configure docker-compose for full stack
- [ ] Test containerized deployment end-to-end
- [ ] Write deployment documentation

## Phase 6: Frontend

- [x] React/Vite frontend with Tailwind CSS
- [x] Dashboard, Predict, History, Performance pages
- [x] Sidebar navigation and Navbar
- [x] API client wired to FastAPI backend
