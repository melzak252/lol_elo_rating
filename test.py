import asyncio
import csv
from dotenv import load_dotenv

load_dotenv()
from database import get_engine
from database.models import *  # noqa: F403
from scrapper.golgg import GolGGScrapper
from playwright.async_api import async_playwright


async def main():
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        scrapper = GolGGScrapper(browser=browser)
        data = await scrapper.get_all_games()
        data = [user.model_dump() for user in data]

        with open("tournaments.csv", mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)


if __name__ == "__main__":
    asyncio.run(main())
