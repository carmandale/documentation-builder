from pathlib import Path
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def examine_apple_doc():
    """Examine actual Apple documentation structure"""
    debug_dir = Path('debug')
    example_file = debug_dir / 'adding-3d-content-to-your-app.html'
    
    if not example_file.exists():
        logger.error(f"Example file not found: {example_file}")
        return
        
    with open(example_file, 'r', encoding='utf-8') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        
        # Examine key structures
        logger.info("\nDocument Structure Analysis:")
        
        # Title structure
        title_elem = soup.find('div', class_='documentation-title')
        if title_elem:
            logger.info(f"\nTitle Structure:")
            logger.info(title_elem.prettify()[:500])
            
        # Code example structure
        code_elem = soup.find('div', class_='code-listing')
        if code_elem:
            logger.info(f"\nCode Example Structure:")
            logger.info(code_elem.prettify()[:500])
            
        # Related topics structure
        related = soup.find(['h2', 'h3'], string=lambda x: x and 'see also' in x.lower())
        if related:
            logger.info(f"\nRelated Topics Structure:")
            logger.info(related.parent.prettify()[:500])

if __name__ == "__main__":
    examine_apple_doc() 