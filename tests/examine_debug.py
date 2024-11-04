from pathlib import Path
from bs4 import BeautifulSoup
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def examine_doc_file(file_path: Path):
    """Examine a single documentation file"""
    logger.info(f"\n\n=== Examining {file_path.name} ===")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        
        # Document Overview
        logger.info("\n=== Document Overview ===")
        
        # Find the main content area
        main_content = soup.find('main')
        if main_content:
            # Extract title and description
            title = main_content.find('h1')
            if title:
                logger.info(f"\nTitle: {title.get_text(strip=True)}")
            
            # Look for description/introduction
            intro = main_content.find(['p', 'div'], class_='introduction')
            if intro:
                logger.info(f"\nIntroduction: {intro.get_text(strip=True)[:200]}...")
        
        # Code Blocks Analysis
        logger.info("\n=== Code Blocks Analysis ===")
        code_blocks = soup.find_all('div', class_='code-listing')
        for i, block in enumerate(code_blocks, 1):
            logger.info(f"\nCode Block {i}:")
            # Get the actual code content
            code_content = block.find('code')
            if code_content:
                # Get the first few lines of code
                code_text = code_content.get_text(strip=True)[:200]
                logger.info(f"Code Preview: {code_text}...")
                
                # Get any associated description
                desc = block.find_previous(['p', 'div'], class_='description')
                if desc:
                    logger.info(f"Description: {desc.get_text(strip=True)}")
        
        # Topics and Navigation
        logger.info("\n=== Topics and Navigation ===")
        topics = soup.find_all(['h2', 'h3'])
        logger.info("\nContent Structure:")
        for topic in topics:
            logger.info(f"- {topic.get_text(strip=True)}")
        
        # Related Content
        logger.info("\n=== Related Content ===")
        related_section = soup.find(['div', 'section'], class_='related')
        if related_section:
            related_links = related_section.find_all('a')
            for link in related_links:
                logger.info(f"Related: {link.get_text(strip=True)} -> {link.get('href', '')}")

        # Return structured data for analysis
        return {
            "filename": file_path.name,
            "title": title.get_text(strip=True) if title else None,
            "num_code_blocks": len(code_blocks),
            "topics": [t.get_text(strip=True) for t in topics],
            "has_related_content": bool(related_section)
        }

def examine_apple_doc():
    """Examine all documentation files in debug directory"""
    debug_dir = Path('debug')
    
    # Find all raw HTML files
    raw_files = list(debug_dir.glob('raw_*.html'))
    
    if not raw_files:
        logger.error("No raw HTML files found in debug directory")
        return
    
    # Analyze each file and collect structured data
    all_data = []
    for file_path in raw_files:
        try:
            data = examine_doc_file(file_path)
            all_data.append(data)
        except Exception as e:
            logger.error(f"Error processing {file_path}: {str(e)}")
    
    # Save combined analysis
    with open(debug_dir / 'structure_analysis.json', 'w') as f:
        json.dump(all_data, f, indent=2)
        logger.info(f"\nStructured analysis saved to {debug_dir / 'structure_analysis.json'}")

if __name__ == "__main__":
    examine_apple_doc() 