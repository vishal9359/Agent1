"""
Configuration loader for the AI Agent
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv


class ConfigLoader:
    """Load and manage configuration settings"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize configuration loader
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
        load_dotenv()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation
        
        Args:
            key_path: Dot-separated path to config value (e.g., 'ollama.llm_model')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def get_ollama_config(self) -> Dict[str, Any]:
        """Get Ollama configuration"""
        return {
            'base_url': os.getenv('OLLAMA_BASE_URL', self.get('ollama.base_url')),
            'llm_model': os.getenv('LLM_MODEL', self.get('ollama.llm_model')),
            'embedding_model': os.getenv('EMBEDDING_MODEL', self.get('ollama.embedding_model')),
            'temperature': self.get('ollama.temperature'),
            'max_tokens': self.get('ollama.max_tokens'),
        }
    
    def get_vectordb_config(self) -> Dict[str, Any]:
        """Get vector database configuration"""
        return {
            'persist_directory': self.get('vectordb.persist_directory'),
            'collection_name': self.get('vectordb.collection_name'),
            'chunk_size': self.get('vectordb.chunk_size'),
            'chunk_overlap': self.get('vectordb.chunk_overlap'),
        }
    
    def get_parsing_config(self) -> Dict[str, Any]:
        """Get code parsing configuration"""
        return {
            'file_extensions': self.get('parsing.file_extensions'),
            'max_file_size_mb': self.get('parsing.max_file_size_mb'),
            'ignore_dirs': self.get('parsing.ignore_dirs'),
        }
    
    def get_flowchart_config(self) -> Dict[str, Any]:
        """Get flowchart configuration"""
        return {
            'output_format': self.get('flowchart.output_format'),
            'output_dir': self.get('flowchart.output_dir'),
            'max_depth': self.get('flowchart.max_depth'),
            'include_comments': self.get('flowchart.include_comments'),
        }

