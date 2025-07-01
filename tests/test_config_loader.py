"""Tests for ConfigLoader class."""

import pytest
import tempfile
import time
import json
import os
from pathlib import Path
from drift_detector.config_loader import ConfigLoader, ConfigLoadError

class TestConfigLoader:
    """Test cases for ConfigLoader class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.loader = ConfigLoader()

    def test_init(self):
        """Test ConfigLoader initialization"""
        assert self.loader.supported_extensions == {'.yaml', '.yml', '.json'}

    def test_validate_file_exists_success(self, tmp_path):
        """Test successful file validation."""
        # Create a temp YAML file
        test_file = tmp_path / "test_config.yaml"
        test_file.write_text("test: value")

        # Should not raise exception
        result = self.loader.validate_file_exists(str(test_file))
        assert isinstance(result, Path)
        assert result.name == "test_config.yaml"

    def test_validate_file_not_found(self):
        """Test validation with non-existent file."""
        with pytest.raises(ConfigLoadError, match="Configuration file not found"):
            self.loader.validate_file_exists("nonexistent_file.yaml")

    def test_validate_unsupported_extension(self, tmp_path):
        """Test validation with unsupported file extension."""
        test_file = tmp_path / "test_config.txt"
        test_file.write_text("test content")

        with pytest.raises(ConfigLoadError, match="Unsupported file extension"):
            self.loader.validate_file_exists(str(test_file))

    def test_validate_directory_instead_of_file(self, tmp_path):
        """Test validation when path points to directory"""
        test_dir = tmp_path / "test_config.yaml"
        test_dir.mkdir()

        with pytest.raises(ConfigLoadError, match="Path is not a file"):
            self.loader.validate_file_exists(str(test_dir))

    def test_load_yaml_success(self, sample_yaml_file):
        """Test successful YAML file loading."""
        result = self.loader.load_yaml(sample_yaml_file)

        assert isinstance(result, dict)
        assert result['server']['host'] == 'localhost'
        assert result['server']['port'] == 8080
        assert result['server']['debug'] is True
        assert result['database']['name'] == 'testdb'
        assert result['features']['feature_a'] is True

    def test_load_yaml_invalid_syntax(self, invalid_yaml_file):
        """Test YAML loading with invalid syntax"""
        with pytest.raises(ConfigLoadError, match="Invalid YAML syntax"):
            self.loader.load_yaml(invalid_yaml_file)

    def test_load_yaml_empty_file(self, tmp_path):
        """Test YAML loading with empty file"""
        empty_file = tmp_path / "empty.yaml"
        empty_file.write_text("")

        result = self.loader.load_yaml(str(empty_file))
        assert result == {}

    def test_load_yaml_non_dict_root(self, tmp_path):
        """Test YAML loading when root is not a dictionary."""
        list_file = tmp_path / "list_root.yaml"
        list_file.write_text("- item1\n- item2\n- item3")

        with pytest.raises(ConfigLoadError, match="must contain a dictionary at root level"):
            self.loader.load_yaml(str(list_file))

    def test_load_json_success(self, sample_json_file):
        """Test successful JSON file loading"""
        result = self.loader.load_json(sample_json_file)

        assert isinstance(result, dict)
        assert result['server']['host'] == 'localhost'
        assert result['server']['port'] == 8080
        assert result['server']['debug'] is True
        assert result['database']['name'] == 'testdb'
        assert result['features']['feature_a'] is True

    def test_load_json_invalid_syntax(self, invalid_json_file):
        """Test JSON loading with invalid syntax"""
        with pytest.raises(ConfigLoadError, match="Invalid JSON syntax"):
            self.loader.load_json(invalid_json_file)
          
    def test_load_json_empty_file(self, tmp_path):
        """Test JSON loading with empty file"""
        empty_file = tmp_path / "empty.json"
        empty_file.write_text("{}")

        result = self.loader.load_json(str(empty_file))
        assert result == {}

    def test_load_json_non_dict_root(self, tmp_path):
        """Test JSON loading when root is not an object."""
        array_file = tmp_path / "array_root.json"
        array_file.write_text('["item1", "item2", "item3"]')

        with pytest.raises(ConfigLoadError, match="must contain an object at root level"):
            self.loader.load_json(str(array_file))

    def test_load_config_yaml_auto_detection(self, sample_yaml_file):
        """Test auto-detection for YAML files"""
        result = self.loader.load_config(sample_yaml_file)
        assert isinstance(result, dict)
        assert 'server' in result

    def test_load_config_json_auto_detection(self, sample_json_file):
        """Test auto-detection for JSON files"""
        result = self.loader.load_config(sample_json_file)
        assert isinstance(result, dict)
        assert 'server' in result

    def test_load_config_yml_extension(self, tmp_path):
        """Test auto-detection for .yml extension"""
        yml_file = tmp_path / "test.yml"
        yml_file.write_text("test: value")

        result = self.loader.load_config(str(yml_file))
        assert result == {"test": "value"}
    
    def test_load_large_file(self, large_config_file):
      """Test loading a large configuration file."""
      result = self.loader.load_config(large_config_file)
      
      assert isinstance(result, dict)
      assert "level_0" in result
      assert len(result["level_0"]["level_1"]["level_2"]["level_3"]["level_4"]["level_5"]["array_data"]) == 100

    @pytest.mark.skipif(os.name == 'nt', reason="Permission tests not reliable on Windows")
    def test_load_permission_denied(self, permission_denied_file):
      """Test handling of permission denied errors."""
      with pytest.raises(ConfigLoadError, match="Permission denied"):
        self.loader.load_config(permission_denied_file)

    def test_custom_exception_inheritance(self):
      """Test that ConfigLoadError is properly inheriting from Exception."""
      assert issubclass(ConfigLoadError, Exception)
    
      try:
        raise ConfigLoadError("test message")
      except Exception as e:
        assert str(e) == "test message"

    def test_loading_performance(self, large_config_file):
        """Test that large files load within reasonable time"""
        start_time = time.time()
        result = self.loader.load_config(large_config_file)
        end_time = time.time()

        assert(end_time - start_time) < 1.0
        assert isinstance(result, dict)

    def test_multiple_loads_same_file(self, sample_yaml_file):
        """Test loading the same file multiple times"""
        results = []

        for _ in range(5):
            result = self.loader.load_config(sample_yaml_file)
            results.append(result)

        for result in results[1:]:
            assert result == results[0]

        
# Pytest fixtures for creating test files
@pytest.fixture
def sample_yaml_file(tmp_path):
    """Create a sample YAML file for testing"""
    content = """
server:
    host: localhost
    port: 8080
    debug: true

database:
    host: db.example.com
    port: 5432
    name: testdb

features:
    feature_a: true
    feature_b: false
"""

    yaml_file = tmp_path / "sample.yaml"
    yaml_file.write_text(content)
    return str(yaml_file)

@pytest.fixture
def sample_json_file(tmp_path):
    """Create a sample JSON file for testing."""
    content = """{
  "server": {
    "host": "localhost",
    "port": 8080,
    "debug": true
  },
  "database": {
    "host": "db.example.com",
    "port": 5432,
    "name": "testdb"
  },
  "features": {
    "feature_a": true,
    "feature_b": false
  }
}"""
    json_file = tmp_path / "sample.json"
    json_file.write_text(content)
    return str(json_file)

@pytest.fixture
def invalid_yaml_file(tmp_path):
    """Create an invalid YAML file for testing."""
    content = """
server:
  host: localhost
  port: 8080
  debug: true
    invalid_indentation: value
database:
  - invalid
  - yaml: structure
"""
    yaml_file = tmp_path / "invalid.yaml"
    yaml_file.write_text(content)
    return str(yaml_file)


@pytest.fixture
def invalid_json_file(tmp_path):
    """Create an invalid JSON file for testing."""
    content = """{
  "server": {
    "host": "localhost",
    "port": 8080,
    "debug": true,
  },
  "database": {
    "host": "db.example.com"
    "port": 5432
  }
}"""
    json_file = tmp_path / "invalid.json"
    json_file.write_text(content)
    return str(json_file)

@pytest.fixture
def permission_denied_file(tmp_path):
    """Create a file with restricted permissions (Unix only)."""
    import os
    import stat
    
    restricted_file = tmp_path / "restricted.yaml"
    restricted_file.write_text("test: value")
    
    # Remove read permissions (Unix only)
    if os.name != 'nt':  # Not Windows
        os.chmod(restricted_file, stat.S_IWRITE)
    
    return str(restricted_file)

@pytest.fixture
def large_config_file(tmp_path):
    """Create a large configuration file for testing."""
    content = {"level_0": {}}
    current = content["level_0"]
    
    # Create nested structure
    for i in range(5):
        current[f"level_{i+1}"] = {}
        current[f"data_{i}"] = f"value_{i}"
        current = current[f"level_{i+1}"]
    
    # Add arrays and various data types
    current["array_data"] = list(range(100))
    current["string_data"] = "test_string"
    current["boolean_data"] = True
    current["null_data"] = None
    current["number_data"] = 42.5
    
    large_file = tmp_path / "large_config.json"
    with open(large_file, 'w') as f:
        json.dump(content, f, indent=2)
    
    return str(large_file)