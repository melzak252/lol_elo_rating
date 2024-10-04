import asyncio
from typing import List
from playwright.async_api import Page, Browser, ElementHandle
from urllib.parse import urljoin, quote

from database.schemas import TournamentBase, TournamentCreate


TOURNAMENT_LIST_URL = "https://gol.gg/tournament/list/"
BASE_TOURNAMENT_URL = "https://gol.gg/tournament/"
BASE_GAME_URL = "https://gol.gg/game/"
BASE_TEAMS_URL = "https://gol.gg/teams/"
BASE_PLAYERS_URL = "https://gol.gg/players/"


class GolGGScrapper:
    def __init__(self, browser: Browser) -> None:
        self.browser: Browser = browser

    async def handle_game_page(self, page: Page):
        pass

    async def handle_season_page(self, page: Page):
        tournaments_list = await page.query_selector("table.table_list")
        tournament_links = await tournaments_list.query_selector_all("a")

        for t_link in tournament_links:
            href: str = await t_link.get_attribute("href")
            href = href.removeprefix(".")
            t_page: Page = await self.browser.new_page()
            await t_page.goto(f"{self.BASE_TOURNAMENT_URL}{href}")
            await self.handle_consent_dialog(t_page)

            nav_element = await t_page.wait_for_selector(
                "//li[contains(@class, 'game-menu-button2')]//a[text()='Match list']",
                timeout=5000,
            )

            await nav_element.click()

            table = await t_page.wait_for_selector("table.table_list")
            matches = await table.query_selector_all("a")
            for match in matches:
                match_href = await match.get_attribute("href")
                full_url = urljoin(BASE_TOURNAMENT_URL, match_href)

                match_page: Page = await self.browser.new_page()
                await match_page.goto(full_url)
                await self.handle_consent_dialog(match_page)
                await asyncio.sleep(5)
                await page.close()
                break

            await asyncio.sleep(10)
            await t_page.close()
            break

    @staticmethod
    async def handle_consent_dialog(page: Page):
        try:
            await page.wait_for_selector("button.fc-button", timeout=5000)
            await page.click("button.fc-button")
            print("Consent dialog handled")
        except Exception as e:
            print("No consent dialog found or error occurred:", e)

    async def get_all_tournaments(self) -> List[TournamentBase]:
        page = await self.browser.new_page()

        await page.goto(TOURNAMENT_LIST_URL)
        await self.handle_consent_dialog(page)

        await page.wait_for_selector("li.season-link")

        seassons = await page.query_selector_all("li.season-link")

        scrapped_data = []
        for seasson_link in seassons:
            print(f"Scraping seasson {await seasson_link.inner_text()}")
            await seasson_link.click()

            tournaments_table = await page.wait_for_selector("table.table_list")
            tournament_rows: List[ElementHandle] = (
                await tournaments_table.query_selector_all("tbody tr")
            )
            for row in tournament_rows:
                cols = await row.query_selector_all("td")
                _, name, region, no_games, _, first_game, last_game, *_ = cols
                tournament_link = await name.query_selector("a")
                tournament_href = await tournament_link.get_attribute("href")
                tournament_url = quote(
                    urljoin(BASE_TOURNAMENT_URL, tournament_href), safe=":/"
                )
                tournament_name = await name.inner_text()
                tournament_region = await region.inner_text()
                number_of_games = int(await no_games.inner_text())
                first_game = await first_game.inner_text()
                last_game = await last_game.inner_text()

                tournament = TournamentCreate(
                    name=tournament_name,
                    source=tournament_url,
                    region=tournament_region,
                    number_of_games=number_of_games,
                    start_date=first_game,
                    end_date=last_game,
                )

                scrapped_data.append(tournament)

            # await self.handle_season_page(page)
        await page.close()
        return scrapped_data
