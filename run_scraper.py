import asyncio
import signal
from documentation_scraper import VisionOSScraper
import logging
import sys

logger = logging.getLogger(__name__)

async def main():
    scraper = VisionOSScraper()
    
    def handle_interrupt(signum, frame):
        logger.info("Interrupt received, stopping scraper...")
        scraper.stop()
    
    # Register signal handlers
    signal.signal(signal.SIGINT, handle_interrupt)
    signal.signal(signal.SIGTERM, handle_interrupt)
    
    try:
        await scraper.run()
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
    finally:
        logger.info("Scraping complete")
        # Force exit to kill any hanging processes
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main()) 