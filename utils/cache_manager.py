from pathlib import Path
from typing import List
from utils.logging import logger

class CacheManager:
    """Centralized cache management"""
    
    def __init__(self, base_dir: Path = Path('data')):
        self.base_dir = base_dir
        self.cache_dir = base_dir / 'cache'
        self.knowledge_dir = base_dir / 'knowledge'
        self.logs_dir = base_dir / 'logs'
        
        # Create directories
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Define ALL cache files in one place
        self.cache_files = {
            'url_cache': self.cache_dir / 'url_cache.json',
            'samples_cache': self.cache_dir / 'discovered_samples.json',
            'doc_cache': self.cache_dir / 'documentation_cache.json',
            'analysis_cache': self.cache_dir / 'analysis_cache.json',
            'relationships': self.knowledge_dir / 'relationships.json'
        }
    
    def clear_all(self):
        """Clear all cache files, sample downloads, and logs"""
        logger.info("Clearing all cache files...")
        
        # Clear cache files
        for name, file_path in self.cache_files.items():
            try:
                if file_path.exists():
                    logger.info(f"Removing {name} cache: {file_path}")
                    file_path.unlink()
            except Exception as e:
                logger.error(f"Error removing {file_path}: {str(e)}")
            
        # Clear old sample downloads directory
        samples_dir = self.cache_dir / 'samples'
        if samples_dir.exists():
            try:
                import shutil
                shutil.rmtree(samples_dir)
                logger.info(f"Removed old samples directory: {samples_dir}")
            except Exception as e:
                logger.error(f"Error removing samples directory: {str(e)}")
                
        # Clear log file
        log_file = self.logs_dir / 'scraper.log'
        try:
            if log_file.exists():
                logger.info(f"Removing log file: {log_file}")
                log_file.unlink()
        except Exception as e:
            logger.error(f"Error removing log file: {str(e)}")
            
        # Ensure directories exist after clearing
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)