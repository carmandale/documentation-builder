import asyncio
from core.scraper import DocumentationScraper
from core.url_sources import DocumentationURLCollector
from analyzers.project_analyzer import ProjectAnalyzer
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('scraper.log')
    ]
)
logger = logging.getLogger(__name__)

async def main():
    # Initialize collectors
    url_collector = DocumentationURLCollector()
    project_analyzer = ProjectAnalyzer()
    
    # Test subset of URLs
    test_urls = [
        # Core 3D/Animation examples
        "https://developer.apple.com/documentation/visionos/bot-anist",
        "https://developer.apple.com/documentation/visionos/creating-3d-shapes-in-visionos-with-realitykit",
        "https://developer.apple.com/documentation/visionos/creating-an-interactable-3d-model-in-visionos",
        
        # Sample Apps
        "https://developer.apple.com/documentation/visionos/swift-splash",
        "https://developer.apple.com/documentation/visionos/diorama"
    ]
    
    try:
        logger.info("Starting subset test with 5 documentation pages...")
        
        # Process each URL
        downloaded_projects = []
        for url in test_urls:
            logger.info(f"\nProcessing: {url}")
            project = await url_collector.process_documentation_page(url)
            
            if project:
                logger.info(f"Found project: {project.title}")
                await url_collector.download_project(project)
                
                if project.local_path:
                    logger.info(f"Downloaded to: {project.local_path}")
                    downloaded_projects.append(project)
        
        # Analyze downloaded projects
        logger.info("\nAnalyzing downloaded projects:")
        for project in downloaded_projects:
            logger.info(f"\nAnalyzing {project.title}:")
            analysis = project_analyzer.analyze_project(project.local_path)
            
            # Log findings
            logger.info(f"Found patterns:")
            for category, patterns in analysis['patterns'].items():
                if patterns:
                    logger.info(f"- {category}: {len(patterns)} patterns")
                    for pattern in patterns:
                        logger.info(f"  • {pattern['type']} in {pattern['file']}")
            
            # Log pattern usage
            logger.info("\nPattern usage frequency:")
            for pattern, count in analysis['usage'].items():
                logger.info(f"- {pattern}: used {count} times")
        
        logger.info("\nSubset test complete!")
            
    except Exception as e:
        logger.error(f"Error in subset test: {str(e)}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main())