import pytest
from pathlib import Path
from bs4 import BeautifulSoup
from extractors.doc_extractor import DocumentationExtractor
from extractors.code_extractor import CodeBlockExtractor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture
def debug_dir():
    return Path('debug')

@pytest.fixture
def doc_files(debug_dir):
    files = list(debug_dir.glob('raw_*.html'))
    if not files:
        pytest.skip("No raw HTML files found for testing")
    return files

@pytest.fixture
def doc_extractor():
    return DocumentationExtractor()

def test_code_block_extraction(doc_files):
    """Test extraction of code blocks from documentation"""
    for file_path in doc_files:
        logger.info(f"\nTesting code block extraction for {file_path.name}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        code_blocks = CodeBlockExtractor.extract_code_blocks(soup)
        
        assert len(code_blocks) > 0, "Should find at least one code block"
        
        for i, block in enumerate(code_blocks):
            logger.info(f"\nCode Block {i + 1}:")
            logger.info(f"Language: {block.language}")
            logger.info(f"Preview: {block.preview}")
            logger.info(f"Has description: {bool(block.description)}")
            
            assert block.code, "Code block should have content"
            assert block.language == "swift", "Language should be swift for visionOS"
            assert len(block.preview) <= 200, "Preview should be limited to 200 chars"

def test_full_page_extraction(doc_files, doc_extractor):
    """Test extraction of complete documentation pages"""
    for file_path in doc_files:
        logger.info(f"\nTesting full page extraction for {file_path.name}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        url = f"https://developer.apple.com/documentation/visionos/{file_path.stem.replace('raw_', '')}"
        page = doc_extractor.extract_page(soup, url)
        
        assert page is not None, "Should successfully extract page"
        assert page.title, "Page should have a title"
        assert page.url == url, "Page should have correct URL"
        assert len(page.code_blocks) > 0, "Page should have code blocks"
        assert len(page.topics) > 0, "Page should have topics"
        
        logger.info(f"Title: {page.title}")
        logger.info(f"Number of code blocks: {len(page.code_blocks)}")
        logger.info(f"Number of topics: {len(page.topics)}")
        logger.info(f"Has introduction: {bool(page.introduction)}")
        
        # Save extracted data for manual verification
        output_dir = Path('debug/extracted')
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / f"extracted_{file_path.stem.replace('raw_', '')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            # Using model_dump_json instead of deprecated json method
            json_data = page.model_dump_json(indent=2)
            f.write(json_data)
        logger.info(f"Saved extracted data to {output_file}")

def test_topic_extraction(doc_files, doc_extractor):
    """Test extraction of topics and their content"""
    for file_path in doc_files:
        logger.info(f"\nTesting topic extraction for {file_path.name}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        url = f"https://developer.apple.com/documentation/visionos/{file_path.stem.replace('raw_', '')}"
        page = doc_extractor.extract_page(soup, url)
        
        assert page is not None
        assert len(page.topics) > 0
        
        for topic in page.topics:
            logger.info(f"\nTopic: {topic.title}")
            logger.info(f"Level: {topic.level}")
            if topic.content:
                logger.info(f"Content preview: {topic.content[:100]}...")
            
            assert topic.title, "Topic should have a title"
            assert topic.level in [2, 3], "Topic level should be 2 or 3"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])