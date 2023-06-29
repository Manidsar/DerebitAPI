import asyncio

from aiohttp import ClientSession


from utils import AIOHandler


async def main():
    client = ClientSession
    crypp = AIOHandler()

    async with client() as session:
        await asyncio.gather(*[crypp.get_price(session, "btc_usd"), crypp.get_price(session, "eth_usd")],
                             return_exceptions=False)


if __name__ == '__main__':

    asyncio.run(main())
