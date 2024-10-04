from playwright.async_api import async_playwright
from .golgg import GolGGScrapper

browser = None


async def start_browser():
    global browser
    if browser is None:
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=True)


async def get_browser():
    global browser
    if browser is None:
        await start_browser()

    return browser


async def get_golgg_scrapper() -> GolGGScrapper:
    browser = await get_browser()
    return GolGGScrapper(browser)


async def close_browser():
    global browser
    if browser:
        await browser.close()
