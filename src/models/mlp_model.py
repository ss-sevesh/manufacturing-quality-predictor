"""MLP model architecture for quality score prediction.

Defines the Multi-Layer Perceptron regressor using Keras,
with configurable layer sizes, dropout, and activation functions.
"""

import logging
from typing import Dict, List

import tensorflow as tf
from tensorflow import keras

logger = logging.getLogger(__name__)


def build_mlp(
    input_dim: int,
    hidden_layers: List[int],
    dropout_rate: float = 0.3,
    activation: str = "relu",
    output_activation: str = "sigmoid",
    learning_rate: float = 0.001,
    loss: str = "mse",
    metrics: List[str] = None,
) -> keras.Model:
    """Build and compile an MLP regression model.

    Args:
        input_dim: Number of input features.
        hidden_layers: List of neuron counts for each hidden layer.
        dropout_rate: Dropout rate between layers.
        activation: Activation function for hidden layers.
        output_activation: Activation function for output layer.
        learning_rate: Learning rate for Adam optimizer.
        loss: Loss function name.
        metrics: List of metric names to track.

    Returns:
        Compiled Keras Model.
    """
    if metrics is None:
        metrics = ["mae", "mse"]

    model = keras.Sequential(name="quality_predictor_mlp")
    model.add(keras.layers.Input(shape=(input_dim,)))

    for i, units in enumerate(hidden_layers):
        model.add(keras.layers.Dense(units, activation=activation, name=f"dense_{i}"))
        model.add(keras.layers.Dropout(dropout_rate, name=f"dropout_{i}"))

    model.add(keras.layers.Dense(1, activation=output_activation, name="output"))

    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

    logger.info(f"Built MLP: input={input_dim}, layers={hidden_layers}, dropout={dropout_rate}")
    return model


def build_mlp_from_config(config: Dict) -> keras.Model:
    """Build MLP model from a configuration dictionary.

    Args:
        config: Dictionary with 'model' section containing
                'architecture' and 'hyperparameters' subsections.

    Returns:
        Compiled Keras Model.
    """
    arch = config["model"]["architecture"]
    hyper = config["model"]["hyperparameters"]

    return build_mlp(
        input_dim=arch["input_dim"],
        hidden_layers=arch["hidden_layers"],
        dropout_rate=arch["dropout_rate"],
        activation=arch["activation"],
        output_activation=arch["output_activation"],
        learning_rate=hyper["learning_rate"],
        loss=hyper["loss"],
        metrics=hyper["metrics"],
    )


def get_callbacks(config: Dict) -> list:
    """Create training callbacks from config.

    Args:
        config: Dictionary with 'model.callbacks' section.

    Returns:
        List of Keras callback instances.
    """
    cb_config = config["model"]["callbacks"]
    callbacks = []

    if "early_stopping" in cb_config:
        es = cb_config["early_stopping"]
        callbacks.append(
            keras.callbacks.EarlyStopping(
                patience=es["patience"],
                monitor=es["monitor"],
                restore_best_weights=es["restore_best_weights"],
            )
        )

    if "reduce_lr" in cb_config:
        rl = cb_config["reduce_lr"]
        callbacks.append(
            keras.callbacks.ReduceLROnPlateau(
                factor=rl["factor"],
                patience=rl["patience"],
                min_lr=rl["min_lr"],
            )
        )

    if "model_checkpoint" in cb_config:
        mc = cb_config["model_checkpoint"]
        import os
        os.makedirs(os.path.dirname(mc["filepath"]), exist_ok=True)
        callbacks.append(
            keras.callbacks.ModelCheckpoint(
                filepath=mc["filepath"],
                monitor=mc["monitor"],
                save_best_only=mc["save_best_only"],
                save_weights_only=mc.get("save_weights_only", False),
            )
        )

    return callbacks
