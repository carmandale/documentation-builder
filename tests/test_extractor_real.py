import pytest
from pathlib import Path
from bs4 import BeautifulSoup
from extractors.base_extractor import BaseExtractor

def load_real_doc(filename: str = "adding-3d-content-to-your-app.html") -> str:
    """Load a real Apple documentation file"""
    debug_dir = Path('debug')
    file_path = debug_dir / filename
    
    if not file_path.exists():
        pytest.skip(f"Test file not found: {file_path}")
        
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

@pytest.mark.asyncio
async def test_extract_from_real_doc():
    """Test extraction from real documentation"""
    test_file = Path('data/documentation/adding-3d-content-to-your-app.json')
    
    if not test_file.exists():
        pytest.skip(f"Test file not found: {test_file}")
        
    content = load_real_doc()
    soup = BeautifulSoup(content, 'html.parser')
    extractor = BaseExtractor()
    
    entry = extractor.extract(soup)
    
    assert entry is not None
    assert entry.title == "Adding 3D Content to Your App"
    assert "3D" in entry.description
    assert len(entry.examples) > 0
    
    # Test code example extraction
    first_example = entry.examples[0]
    assert "RealityView" in first_example.code
    assert "RealityKit" in first_example.frameworks
    
    # Test related topics
    assert len(entry.related_topics) > 0
    
    # Test prerequisites
    assert len(entry.prerequisites) > 0 