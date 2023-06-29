from fastapi import FastAPI
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter


from utils import APIV1Handler


apiv1 = FastAPI()
app = FastAPI()
app.mount("/api/v1", apiv1)
router = InferringRouter()


@cbv(router)
class ExternalAPI:
    _handler = APIV1Handler()

    @router.get("/get_date_price/{request_date}")
    async def get_date_price(self, ticker: str, request_date: str) -> dict:
        """
        This method get you date filter ticker

        param request_date: format: YYYY-MM-DD
        for example 2023-06-28

        param ticker: btc_usd or eth_usd
        """

        message = await self._handler.get_date_price(ticker, request_date)
        return message

    @router.get("/get_last_price")
    async def get_last_price(self, ticker: str) -> dict:
        """This method get you last ticker's price

        param ticker: btc_usd or eth_usd
        """
        message = await self._handler.get_last_price(ticker)
        return message

    @router.get("/get_all")
    async def get_all(self, ticker: str) -> dict:
        """This method get you all prices for request ticker

        param ticker: btc_usd or eth_usd
        """
        message = await self._handler.get_all(ticker)
        return message


apiv1.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
