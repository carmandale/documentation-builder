import asyncio
from playwright.async_api import async_playwright
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Test basic URL access"""
    urls = [
        "https://developer.apple.com/documentation/visionos/adding-3d-content-to-your-app",
        "https://developer.apple.com/documentation/visionos/creating-your-first-visionos-app"
    ]
    
    debug_dir = Path('debug')
    debug_dir.mkdir(exist_ok=True)
    
    playwright = None
    browser = None
    
    try:
        playwright = await async_playwright().start()
        # Launch browser with specific options for stability
        browser = await playwright.chromium.launch(
            headless=True,  # Changed to headless mode for better stability
        )
        
        # Create a new context with specific viewport and user agent
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        
        # Create a new page in this context
        page = await context.new_page()
        
        for url in urls:
            try:
                logger.info(f"Testing access to: {url}")
                
                # Navigate with explicit wait state
                response = await page.goto(
                    url,
                    wait_until='networkidle',
                    timeout=30000
                )
                
                if response:
                    logger.info(f"Status: {response.status}")
                    logger.info(f"Content type: {response.headers.get('content-type', 'unknown')}")
                
                    # Take a screenshot after content loads
                    screenshot_path = debug_dir / f"test_{url.split('/')[-1]}.png"
                    await page.screenshot(path=str(screenshot_path))
                    logger.info(f"Screenshot saved to {screenshot_path}")
                    
                    # Get content
                    content = await page.content()
                    logger.info(f"Content length: {len(content)}")
                    logger.info(f"Contains 'visionOS': {'visionOS' in content}")
                    
                    # Save raw HTML for analysis
                    html_path = debug_dir / f"raw_{url.split('/')[-1]}.html"
                    with open(html_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                else:
                    logger.error(f"No response received for {url}")
                
                await asyncio.sleep(2)  # Brief pause between URLs
                
            except Exception as e:
                logger.error(f"Error accessing {url}: {str(e)}")
                
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        
    finally:
        logger.info("Cleaning up browser resources...")
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()

if __name__ == "__main__":
    asyncio.run(main())