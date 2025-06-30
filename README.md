# Configuration Drift Detector

A Python tool for detecting configuration drift between different environments (dev, staging, production).

## Project Status
🚧 **Work in Progress** - This project is being actively developed as part of a DevOps-to-Software-Engineering transition.

## Goals
- Detect configuration differences between environments
- Support multiple configuration formats (YAML, JSON)
- Generate human-readable drift reports
- Provide CLI interface for automation
- Demonstrate clean Python architecture and testing practices

## Planned Features
- [x] Project setup and structure
- [ ] Configuration file loading (YAML, JSON)
- [ ] Drift detection algorithm
- [ ] CLI interface
- [ ] Report generation
- [ ] Automated remediation capabilities

## Development Setup

### Prerequisites
- Python 3.8+
- Git

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/config-drift-detector.git
cd config-drift-detector

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .

# Running tests
pytest

# Project structure
config-drift-detector/
├── src/drift_detector/       # Main package
├── tests/                    # Test files
├── sample_configs/           # Example configuration files
├── docs/                     # Documentation
└── requirements.txt          # Dependencies

# Compare two configuration files
drift-detector detect --source prod_config.yaml --target staging_config.yaml

# Generate JSON report
drift-detector detect --source config1.yaml --target config2.yaml --output-format json