import asyncio
from core.scraper import DocumentationScraper
import logging
from pathlib import Path

# Configure logging with more detail
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Print to console
        logging.FileHandler('scraper.log')  # Also save to file
    ]
)
logger = logging.getLogger(__name__)

async def main():
    scraper = DocumentationScraper()
    try:
        # Use verified working URLs
        test_urls = [
            "https://developer.apple.com/documentation/visionos/adding-3d-content-to-your-app",
            "https://developer.apple.com/documentation/visionos/creating-your-first-visionos-app",
            "https://developer.apple.com/documentation/visionos/creating-fully-immersive-experiences",
            "https://developer.apple.com/documentation/visionos/creating-immersive-spaces-in-visionos-with-swiftui",
            "https://developer.apple.com/documentation/visionos/bot-anist",
            "https://developer.apple.com/documentation/visionos/swift-splash"
        ]
        
        logger.info("Initializing scraper...")
        await scraper.init()
        
        # Override the CLI default URLs
        scraper.urls = test_urls
        
        pages = []
        for url in test_urls:
            logger.info(f"Scraping: {url}")
            page = await scraper.scrape_url(url)
            if page:
                pages.append(page)
                logger.info(f"Successfully scraped: {page.title}")
            else:
                logger.error(f"Failed to scrape: {url}")
            
            # Brief pause between requests
            await asyncio.sleep(2)
            
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
    finally:
        logger.info("Cleaning up...")
        await scraper.cleanup()

if __name__ == "__main__":
    logger.info("Starting scraper...")
    asyncio.run(main())
    logger.info("Scraper finished")