# Project Tasks

## Phase 1: Setup & Data

- [ ] Initialize project structure and virtual environment
- [ ] Install all dependencies from requirements.txt
- [ ] Create synthetic manufacturing dataset (generate_data.py)
- [ ] Implement data validation with Great Expectations (validate.py)
- [ ] Build preprocessing pipeline: scaling, encoding, feature engineering (preprocess.py)
- [ ] Run exploratory data analysis notebook (01_eda.ipynb)
- [ ] Write unit tests for data modules

## Phase 2: Model Development

- [ ] Define MLP architecture in Keras (mlp_model.py)
- [ ] Implement training loop with callbacks and checkpointing (train.py)
- [ ] Integrate MLflow experiment tracking into training
- [ ] Run Keras Tuner hyperparameter search
- [ ] Train baseline model and log metrics
- [ ] Write unit tests for model modules

## Phase 3: Evaluation & Explainability

- [ ] Implement evaluation metrics: MAE, RMSE, R2 (evaluate.py)
- [ ] Generate residual plots and prediction vs actual plots
- [ ] Run SHAP analysis for feature importance
- [ ] Create visualization utilities (plots.py)
- [ ] Document model performance in MLflow
- [ ] Write tests for evaluation functions

## Phase 4: API Development

- [ ] Build FastAPI prediction endpoint (main.py)
- [ ] Define request/response schemas with Pydantic (schemas.py)
- [ ] Add health check and model info endpoints
- [ ] Write API integration tests (test_api.py)
- [ ] Test API with sample prediction requests

## Phase 5: Deployment

- [ ] Export trained model to ONNX format
- [ ] Build Docker image for API service
- [ ] Configure docker-compose for full stack
- [ ] Test containerized deployment end-to-end
- [ ] Write deployment documentation

## Phase 6: Monitoring

- [ ] Set up Streamlit dashboard for live predictions
- [ ] Add data drift detection
- [ ] Configure logging and alerting
- [ ] Set up model performance monitoring
- [ ] Document monitoring procedures
