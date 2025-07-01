"""Integration tests for ConfigLoader using real sample files."""

import pytest
from pathlib import Path
from drift_detector.config_loader import ConfigLoader


class TestConfigLoaderIntegration:
    """Integration tests using actual sample configuration files."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.loader = ConfigLoader()
        self.sample_dir = Path(__file__).parent.parent / "sample_configs"
    
    def test_load_sample_yaml_files(self):
        """Test loading actual sample YAML files."""
        prod_file = self.sample_dir / "prod_config.yaml"
        staging_file = self.sample_dir / "staging_config.yaml"
        
        if prod_file.exists():
            prod_config = self.loader.load_config(str(prod_file))
            assert isinstance(prod_config, dict)
            assert "server" in prod_config
            assert "database" in prod_config
        
        if staging_file.exists():
            staging_config = self.loader.load_config(str(staging_file))
            assert isinstance(staging_config, dict)
            assert "server" in staging_config
    
    def test_load_sample_json_files(self):
        """Test loading actual sample JSON files."""
        dev_file = self.sample_dir / "dev_config.json"
        
        if dev_file.exists():
            dev_config = self.loader.load_config(str(dev_file))
            assert isinstance(dev_config, dict)
            assert "server" in dev_config
    
    def test_compare_yaml_and_json_structure(self):
        """Test that YAML and JSON files have compatible structures."""
        yaml_file = self.sample_dir / "staging_config.yaml"
        json_file = self.sample_dir / "dev_config.json"
        
        if yaml_file.exists() and json_file.exists():
            yaml_config = self.loader.load_config(str(yaml_file))
            json_config = self.loader.load_config(str(json_file))
            
            # Both should have server section
            assert "server" in yaml_config
            assert "server" in json_config
            
            # Both should have similar structure
            yaml_keys = set(yaml_config.keys())
            json_keys = set(json_config.keys())
            
            # Should have at least some common keys
            common_keys = yaml_keys.intersection(json_keys)
            assert len(common_keys) > 0