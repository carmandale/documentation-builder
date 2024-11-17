"""Serialization utilities for the documentation builder."""

import json
from pathlib import Path
from typing import Any, Dict, List, Set, Union
from datetime import datetime

class JSONSerializer:
    """JSON serialization helper for complex data types."""
    
    @staticmethod
    def serialize(obj: Any) -> Any:
        """Serialize an object to JSON-compatible format."""
        if isinstance(obj, (set, Set)):
            return list(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, Path):
            return str(obj)
        return obj

    @staticmethod
    def save_json(data: Union[Dict, List], filepath: Union[str, Path], pretty: bool = True) -> None:
        """Save data to a JSON file.
        
        Args:
            data: Data to serialize
            filepath: Path to save JSON file
            pretty: If True, format JSON with indentation
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, default=JSONSerializer.serialize, 
                     indent=2 if pretty else None, 
                     ensure_ascii=False)

    @staticmethod
    def load_json(filepath: Union[str, Path]) -> Union[Dict, List]:
        """Load data from a JSON file.
        
        Args:
            filepath: Path to JSON file
            
        Returns:
            Loaded data structure
        """
        filepath = Path(filepath)
        if not filepath.exists():
            return {}
            
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
