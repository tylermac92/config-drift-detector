"""
Configuration Drift Detection Tool

A Python package for detecting configuration drift between environments.
"""

__version__ = "0.1.0"
__author__ = "Your Name"

# Import main classes for easy access
from .config_loader import ConfigLoader, ConfigLoadError
from .drift_analyzer import DriftAnalyzer

__all__ = ["ConfigLoader", "ConfigLoadError", "DriftAnalyzer"]