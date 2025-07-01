"""
Configuration file loading utilities.

This module provides the ConfigLoader class for loading and parsing
configuration files in YAML and JSON formats. It includes comprehensive
error handling, validation, and automatic format detection.

Classes:
    ConfigLoadError: Custom exception for configuration loading errors
    ConfigLoader: Main class for loading configuration files

Example:
    Basic usage:
    
    >>> from drift_detector.config_loader import ConfigLoader
    >>> loader = ConfigLoader()
    >>> config = loader.load_config("my_config.yaml")
    >>> print(config)
"""

import yaml
import json
from pathlib import Path
from typing import Dict, Any
import logging

# Set up logging
logger = logging.getLogger(__name__)

class ConfigLoadError(Exception):
    """Custom exception for configuration loading errors."""
    pass

class ConfigLoader:
    """Handles loading config files from various formats."""

    def __init__(self):
        """Initializes the ConfigLoader."""
        self.supported_extensions = {'.yaml', '.yml', '.json'}

    def validate_file_exists(self, file_path: str) -> Path:
        """
        Validate that file exists and is readable.

        Args:
            file_path: Path to the file to validate

        Returns:
            Path object for the validated file

        Raises:
            ConfigLoadError: If file doesn't exist or isn't readable
        """
        path = Path(file_path)

        if not path.exists():
            raise ConfigLoadError(f"Configuration file not found: {file_path}")

        if not path.is_file():
            raise ConfigLoadError(f"Path is not a file: {file_path}")

        if not path.suffix.lower() in self.supported_extensions:
            raise ConfigLoadError(
                f"Unsupported file extension: {path.suffix}. "
                f"Supported: {', '.join(self.supported_extensions)}"
            )
        
        try:
            # Test if file is readable
            with open(path, 'r') as f:
                pass
        except PermissionError:
            raise ConfigLoadError(f"Permission denied reading file: {file_path}")
        except Exception as e:
            raise ConfigLoadError(f"Error accessing file {file_path}: {str(e)}")

        logger.info(f"File validation successful: {file_path}")
        return path

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
        validated_path = self.validate_file_exists(file_path)

        try:
            with open(validated_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)

            if data is None:
                logger.warning(f"YAML file is empty: {file_path}")
                return {}
            
            if not isinstance(data, dict):
                raise ConfigLoadError(
                    f"YAML file must contain a dictionary at root level, got {type(data).__name__}: {file_path}"
                )
            logger.info(f"Successfully loaded YAML file: {file_path}")
            return data
        except yaml.YAMLError as e:
            raise ConfigLoadError(f"Invalid YAML syntax in {file_path}: {str(e)}")
        except Exception as e:
            raise ConfigLoadError(f"Unexpected error loading YAML file {file_path}: {str(e)}")

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
        validated_path = self.validate_file_exists(file_path)

        try:
            with open(validated_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ConfigLoadError(
                    f"JSON file must contain an object at root level, got {type(data).__name__}: {file_path}"
                )
            
            logger.info(f"Successfully loaded JSON file: {file_path}")
            return data
        
        except json.JSONDecodeError as e:
            raise ConfigLoadError(f"Invalid JSON syntax in {file_path}: {str(e)}")
        except Exception as e:
            raise ConfigLoadError(f"Unexpected error loading JSON file {file_path}: {str(e)}")
        
    def load_config(self, file_path: str) -> Dict[str, Any]:
        """
        Load configuration file with automatic format detection.

        Args:
            file_path: Path to the config file

        Returns:
            Dictionary containing the config

        Raises:
            ConfigLoadError: If file loading or parsing fails
        """
        validated_path = self.validate_file_exists(file_path)
        extension = validated_path.suffix.lower()

        if extension in {'.yaml', '.yml'}:
            return self.load_yaml(file_path)
        elif extension == '.json':
            return self.load_json(file_path)
        else:
            raise ConfigLoadError(f"Unsupported file format: {extension}")