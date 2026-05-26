"""Model training pipeline with MLflow tracking.

Orchestrates data loading, model building, training, and artifact logging.
Every training run is tracked in MLflow for reproducibility.
"""

import logging
from pathlib import Path

import mlflow
import mlflow.keras
import tensorflow as tf
import yaml

from src.data.preprocess import preprocess_pipeline
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

        # Log metrics
        for name, value in test_metrics.items():
            mlflow.log_metric(f"test_{name}", value)

        # Log training history
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

        logger.info(f"Training complete. Test metrics: {test_metrics}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    train()
