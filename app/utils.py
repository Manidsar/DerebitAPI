import asyncio
import json
from datetime import date

from aiohttp import ClientSession
import aiohttp.client_exceptions

from database import AIOConnector, APIConnector


class AIOHandler:
    __counter = 0

    _URl = "https://www.deribit.com/api/v2"
    _message = {
        "method": "public/get_index_price",
        "params": {},
        "jsonrpc": "2.0",
    }

    async def get_price(self, session: ClientSession, ticker: str):
        base = AIOConnector()
        while True:
            async with session.post(self._URl, data=json.dumps(self.create_message(ticker))) as resp:

                if resp.status == 200:
                    price = await self.clean_response(resp)
                    await base.save_to_db(ticker, price)
                await asyncio.sleep(60)

    def create_message(self, ticker: str):
        self.__counter += 1
        self._message["params"]["index_name"] = ticker
        self._message["id"] = self.__counter
        return self._message

    @staticmethod
    async def clean_response(response: aiohttp.client_exceptions.ClientResponse) -> float:
        data = await response.json()
        price = data["result"]["estimated_delivery_price"]
        return price


class APIV1Handler:
    _connector = APIConnector()

    async def get_last_price(self, ticker: str) -> dict:
        """ Тут будет проверка на нормальные значения и так далее"""

        record_lats = await self._connector.get_last_price(ticker=ticker)
        record_lats = record_lats.scalar()
        correct_data = await self.get_data(record_lats)

        return correct_data

    async def get_date_price(self, ticker: str, data: str):

        my_date = date.fromisoformat(data)
        record_date = await self._connector.get_date_price(ticker=ticker, data=my_date)
        record_date = record_date.scalars().all()
        correct_data = await self.get_data(record_date)

        return correct_data

    async def get_all(self, ticker):
        record_all = await self._connector.get_all(ticker)
        record_all = record_all.scalars().all()
        correct_data = await self.get_data(record_all)

        return correct_data

    @staticmethod
    async def get_data(data: dict) -> dict:

        message = {"v": "v1", "data": data}
        return message
