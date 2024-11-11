import pytest
import asyncio
from pathlib import Path
from core.url_sources import URLSources, DocumentationURLCollector
from core.documentation_analyzer import DocumentationAnalyzer
from core.config import TESTING_MODE, TEST_SAMPLE_COUNT
from utils.logging import logger

@pytest.mark.skip(reason="URL discovery tests temporarily disabled")
@pytest.mark.asyncio
async def test_url_discovery():
    """Test URL discovery functionality"""
    url_collector = DocumentationURLCollector()
    test_url = "https://developer.apple.com/documentation/visionos/creating-your-first-visionos-app"
    
    logger.info(f"Starting URL discovery test in testing mode")
    links = await url_collector.get_documentation_links(test_url)
    
    # In testing mode, should only process TEST_SAMPLE_COUNT links
    assert len(links) <= TEST_SAMPLE_COUNT if TESTING_MODE else True
    assert 'documentation' in links
    
    # Test structure analysis
    structure = await url_collector.analyze_documentation_structure(test_url)
    assert structure
    assert 'sections' in structure

@pytest.mark.asyncio
async def test_pattern_analysis():
    """Test pattern analysis functionality"""
    doc_analyzer = DocumentationAnalyzer(Path('data/knowledge'))
    test_content = """
    struct ContentView: View {
        var body: some View {
            RealityView {
                // 3D content
            }
            .gesture(TapGesture())
            .animation(.default)
        }
    }
    """
    
    patterns = doc_analyzer.analyze_code_patterns(test_content, "test_url")
    assert patterns
    assert any(p['type'] == 'ui_components' for p in patterns)
    assert any(p['type'] == '3d_content' for p in patterns)
    assert any(p['type'] == 'gestures' for p in patterns) 