from setuptools import setup, find_packages

setup(
    name="drift-detector",
    version="0.1.0",
    description="A Python tool for detecting configuration drift",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "pyyaml>=6.0",
        "click>=8.0",
        "colorama>=0.4.4",
    ],
    entry_points={
        "console_scripts": [
            "drift-detector=drift_detector.cli:main",
        ],
    },
)