"""Configuration file loading utilities."""

import yaml
import json
from pathlib import Path
from typing import Dict, Any

class ConfigLoader:
    """Handles loading config files from various formats."""

    def __init__(self):
        """Initializes the ConfigLoader."""
        pass

    def load_yaml(self, file_path: str) -> Dict[str, Any]:
        """
        Load config from a YAML file.

        Args:
            file_path: Path to the YAML file

        Returns:
            Dictionary containing the configuration

        Raises:
            FileNotFoundError: If the file doesn't exist
            yaml.YAMLError: If the file contains invalid YAML
        """
        # TODO: Implement in Day 3-4
        raise NotImplementedError("Will implement in Day 3-4")

    def load_json(self, file_path: str) -> Dict[str, Any]:
        """
        Load config from a JSON file.

        Args:
            file_path: Path to the JSON file

        Returns:
            Dictionary containing the configuration

        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
        """
        # TODO: Implement in Day 3-4
        raise NotImplementedError("Will implement in Day 3-4")