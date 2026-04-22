"""Synthetic manufacturing data generator.

Generates realistic sensor and process data for manufacturing quality
prediction. Quality score is a nonlinear function of process features
with added Gaussian noise to simulate real-world measurement variability.
"""

import logging
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

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


def generate_manufacturing_data(num_samples: int = 10000, seed: int = 42) -> pd.DataFrame:
    """Generate synthetic manufacturing sensor data.

    Creates a dataset with 15 process features and a nonlinear quality
    score target. Feature distributions and correlations are designed to
    mimic real manufacturing process data.

    Args:
        num_samples: Number of samples to generate.
        seed: Random seed for reproducibility.

    Returns:
        DataFrame with process features and quality_score target column.
    """
    rng = np.random.default_rng(seed)

    data = {
        "temperature": rng.normal(180, 15, num_samples),
        "pressure": rng.normal(45, 5, num_samples),
        "vibration": rng.exponential(0.05, num_samples),
        "humidity": rng.normal(60, 10, num_samples),
        "speed": rng.normal(1200, 100, num_samples),
        "thickness": rng.normal(2.5, 0.3, num_samples),
        "power_consumption": rng.normal(350, 30, num_samples),
        "tool_wear": rng.uniform(0, 1, num_samples),
        "coolant_flow": rng.normal(8, 1.5, num_samples),
        "ambient_temp": rng.normal(24, 3, num_samples),
        "cycle_time": rng.normal(45, 5, num_samples),
        "material_hardness": rng.normal(58, 5, num_samples),
        "spindle_load": rng.normal(70, 10, num_samples),
        "feed_rate": rng.normal(0.25, 0.05, num_samples),
        "surface_roughness": rng.exponential(1.5, num_samples),
    }

    df = pd.DataFrame(data)

    # Quality score as nonlinear function of features
    quality = (
        50
        + 0.15 * (180 - np.abs(df["temperature"] - 180))
        - 3.0 * df["vibration"]
        + 0.1 * (df["pressure"] - 40)
        - 5.0 * df["tool_wear"]
        + 0.05 * df["coolant_flow"]
        - 0.02 * np.abs(df["humidity"] - 55)
        + 0.01 * (df["speed"] - 1100)
        - 0.3 * df["surface_roughness"]
        + 0.05 * df["material_hardness"]
        - 0.02 * np.abs(df["cycle_time"] - 45)
        + rng.normal(0, 2, num_samples)  # measurement noise
    )

    df["quality_score"] = np.clip(quality, 0, 100)

    logger.info(f"Generated {num_samples} samples with {len(df.columns)} columns")
    return df


def save_data(df: pd.DataFrame, output_path: str) -> None:
    """Save DataFrame to CSV.

    Args:
        df: DataFrame to save.
        output_path: File path for the output CSV.
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Data saved to {output_path} ({len(df)} rows)")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    config = load_config()
    df = generate_manufacturing_data(
        num_samples=config["data"]["num_samples"],
        seed=config["data"]["random_seed"],
    )
    save_data(df, config["data"]["raw_path"])
