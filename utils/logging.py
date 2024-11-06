from pathlib import Path
import logging
import sys

def setup_logging(base_dir: Path = Path('data')) -> logging.Logger:
    """Setup logging configuration with both file and console output"""
    
    # Create logs directory
    logs_dir = base_dir / 'logs'
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger('documentation_analyzer')
    logger.setLevel(logging.DEBUG)
    
    # Create formatters
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    
    # File handler - detailed logging
    file_handler = logging.FileHandler(logs_dir / 'scraper.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    
    # Console handler - info level and above
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Create and export default logger
logger = setup_logging() 