"""Model training pipeline with MLflow tracking.

Orchestrates data loading, model building, training, and artifact logging.
Every training run is tracked in MLflow for reproducibility.
"""

import json
import logging
from datetime import datetime
from pathlib import Path

import mlflow
import mlflow.keras
import numpy as np
import tensorflow as tf
import yaml

from src.data.preprocess import preprocess_pipeline
from src.models.evaluate import evaluate_model
from src.models.mlp_model import build_mlp_from_config, get_callbacks

logger = logging.getLogger(__name__)


def load_config(config_path: str = "configs/config.yaml") -> dict:
    """Load configuration from YAML file.

    Args:
        config_path: Path to the YAML configuration file.

    Returns:
        Dictionary containing configuration parameters.
    """
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def train(config_path: str = "configs/config.yaml") -> None:
    """Run the full training pipeline.

    Loads data, builds the MLP, trains with callbacks, and logs
    everything to MLflow including parameters, metrics, and model artifacts.
    Saves a metrics.json file for the API to serve.

    Args:
        config_path: Path to the YAML configuration file.
    """
    config = load_config(config_path)

    seed = config["data"]["random_seed"]
    tf.random.set_seed(seed)

    # Prepare data
    X_train, X_test, y_train, y_test = preprocess_pipeline(
        raw_path=config["data"]["raw_path"],
        processed_dir=config["data"]["processed_dir"],
        scaler_path=config["data"]["scaler_path"],
        target_col=config["data"]["target"],
        test_size=config["data"]["test_size"],
        seed=config["data"]["random_seed"],
    )

    # Set up MLflow
    mlflow.set_tracking_uri(config["mlflow"]["tracking_uri"])
    mlflow.set_experiment(config["mlflow"]["experiment_name"])

    with mlflow.start_run():
        # Log parameters
        mlflow.log_params({
            "hidden_layers": str(config["model"]["architecture"]["hidden_layers"]),
            "dropout_rate": config["model"]["architecture"]["dropout_rate"],
            "learning_rate": config["model"]["hyperparameters"]["learning_rate"],
            "batch_size": config["model"]["hyperparameters"]["batch_size"],
            "epochs": config["model"]["hyperparameters"]["epochs"],
            "optimizer": config["model"]["hyperparameters"]["optimizer"],
            "train_samples": len(X_train),
            "test_samples": len(X_test),
        })

        # Build model
        model = build_mlp_from_config(config)
        model.summary(print_fn=logger.info)

        # Train
        callbacks = get_callbacks(config)
        history = model.fit(
            X_train,
            y_train,
            validation_split=config["training"]["validation_split"],
            batch_size=config["model"]["hyperparameters"]["batch_size"],
            epochs=config["model"]["hyperparameters"]["epochs"],
            callbacks=callbacks,
            shuffle=config["training"]["shuffle"],
            verbose=config["training"]["verbose"],
        )

        # Evaluate on test set
        test_results = model.evaluate(X_test, y_test, verbose=0)
        test_metrics = dict(zip(model.metrics_names, test_results))

        # Log metrics to MLflow
        for name, value in test_metrics.items():
            mlflow.log_metric(f"test_{name}", value)

        for epoch, (loss, val_loss) in enumerate(
            zip(history.history["loss"], history.history["val_loss"])
        ):
            mlflow.log_metric("train_loss", loss, step=epoch)
            mlflow.log_metric("val_loss", val_loss, step=epoch)

        # Save model
        export_path = config["training"]["export_path"]
        Path(export_path).mkdir(parents=True, exist_ok=True)
        model.save(f"{export_path}/model.keras")
        logger.info(f"Model saved to {export_path}/model.keras")

        if config["mlflow"]["log_models"]:
            mlflow.keras.log_model(model, "model")

        # Compute real evaluation metrics (on 0-100 scale)
        eval_metrics = evaluate_model(model, X_test, y_test)

        # Build scatter sample (actual vs predicted, original scale)
        y_pred_all = model.predict(X_test, verbose=0).flatten()
        rng = np.random.default_rng(seed)
        idx = rng.choice(len(y_test), size=min(300, len(y_test)), replace=False)
        scatter_sample = [
            {
                "actual": round(float(y_test[i]) * 100, 2),
                "predicted": round(float(y_pred_all[i]) * 100, 2),
            }
            for i in idx
        ]

        # Save metrics.json for the API /metrics endpoint
        metrics_payload = {
            "mae": round(eval_metrics["mae"], 3),
            "rmse": round(eval_metrics["rmse"], 3),
            "r2": round(eval_metrics["r2"], 4),
            "mape": round(eval_metrics["mape"], 3),
            "training_epochs": len(history.history["loss"]),
            "train_samples": int(len(X_train)),
            "test_samples": int(len(X_test)),
            "loss_history": {
                "train": [round(float(v), 6) for v in history.history["loss"]],
                "val": [round(float(v), 6) for v in history.history["val_loss"]],
            },
            "scatter_sample": scatter_sample,
            "generated_at": datetime.now().isoformat(),
        }

        metrics_path = Path(export_path) / "metrics.json"
        with open(metrics_path, "w") as f:
            json.dump(metrics_payload, f)
        logger.info(f"Metrics saved to {metrics_path}")

        logger.info(f"Training complete. Eval metrics: {eval_metrics}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    train()
