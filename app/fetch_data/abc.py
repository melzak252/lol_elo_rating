import json
from abc import abstractmethod, ABC
from time import sleep
from typing import Dict, List, Callable

import pydantic
import requests
import tqdm as tqdm
from sqlalchemy.orm.session import Session

from app.fetch_data.constants import TEAMS_URL, TEAMS_HEADERS
from app.lol_games.teams.db import create_team
from app.lol_games.teams.schemas import TeamCreate
from db import get_db


class Fetcher(ABC):
    def __init__(self, limit: int = 1000):
        self.limit = limit
        self.data = []

    @property
    @abstractmethod
    def headers(self) -> Dict[str, str]:
        pass

    @property
    @abstractmethod
    def _api_url(self) -> str:
        pass

    def start_fetching(self):
        print(f"{self.__class__.__name__}: Start fetching")
        offset = 0
        results: List[Dict[str, str]] = []
        while (data := requests.get(self._api_url.format(self.limit, offset))).json():
            offset += self.limit

            data = [{self.headers.get(k, k): v for k, v in row.items()} for row in data.json()]

            results.extend(data)
            print(f"{self.__class__.__name__}: Fetched {len(results)} objects")

            self.add_to_db(data)



        self.data = results
        print(f"{self.__class__.__name__}: End fetching")
        return results

    @abstractmethod
    def add_to_db(self, data):
        pass
