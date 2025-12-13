"""
Configuration Loader
"""

import yaml
from pathlib import Path
from typing import Dict, Any


class ConfigLoader:
    """Load configuration from YAML file"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get_config(self) -> Dict[str, Any]:
        """Get full configuration"""
        return self.config
