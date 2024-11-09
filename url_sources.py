from typing import List
import json

def _load_from_cache(self) -> List[ProjectResource]:
    """Load samples from cache"""
    try:
        samples_cache = self.cache_manager.cache_files['samples_cache']
        if not samples_cache.exists():
            logger.debug("Cache file doesn't exist yet")
            return []
            
        cache_data = json.loads(samples_cache.read_text())
        return [ProjectResource.model_validate(p) for p in cache_data.get('samples', [])]
    except Exception as e:
        logger.debug(f"Cache not loaded: {str(e)}")
        return []

def clear_cache(self):
    """Clear all cache files using central cache manager"""
    self.cache_manager.clear_all() 