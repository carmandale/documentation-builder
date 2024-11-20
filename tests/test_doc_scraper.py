import asyncio
import logging
from pathlib import Path
from core.url_sources import DocumentationURLCollector
from core.config import MAX_CRAWL_DEPTH

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'  # Simplified format
)

async def main():
    # Initialize collector
    collector = DocumentationURLCollector()
    
    # Test URL for ECS systems
    url = "https://developer.apple.com/documentation/realitykit/ecs-systems"
    
    print(f"\nTesting documentation crawling with configured max_depth = {MAX_CRAWL_DEPTH}")
    print("-" * 60)
    
    # Test with configured depth
    await collector.cache_documentation_page(url)
    
    # Analyze the cache
    cache = collector._load_doc_content_cache()
    pages = cache.get('pages', {})
    
    print(f"\nTotal pages cached: {len(pages)}")
    
    # Analyze page types and depth distribution
    page_types = {}
    depth_distribution = {}
    
    for url, data in pages.items():
        # Count page types
        page_type = data.get('type', 'unknown')
        page_types[page_type] = page_types.get(page_type, 0) + 1
        
        # Count depth distribution based on URL path segments
        path_depth = len(url.split('/')) - 3  # Subtract scheme and domain
        depth_distribution[path_depth] = depth_distribution.get(path_depth, 0) + 1
    
    print("\nPage types found:")
    for type_name, count in sorted(page_types.items()):
        print(f"- {type_name}: {count} pages")
        
    print("\nDepth distribution:")
    for depth, count in sorted(depth_distribution.items()):
        print(f"- Depth {depth}: {count} pages")

if __name__ == "__main__":
    asyncio.run(main())
