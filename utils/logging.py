from pathlib import Path
import logging

def setup_logging(base_dir: Path = Path('data')):
    """Setup logging configuration"""
    # Create logs directory if it doesn't exist
    logs_dir = base_dir / 'logs'
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(logs_dir / 'scraper.log')
        ]
    )

logger = setup_logging() 