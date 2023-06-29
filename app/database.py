import datetime
from dataclasses import dataclass
from time import time

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine, engine
from sqlalchemy.ext.asyncio import async_sessionmaker

import models


@dataclass
class ProxyBase:
    """Make connections with base"""
    _URL: str = 'postgresql+asyncpg://postgres:ZT?78Scvx@localhost:5433/database_test'
    _db_engine: engine = create_async_engine(_URL, echo=True)

    @classmethod
    async def create_db_if_not_exist(cls):
        async with cls._db_engine.begin() as conn:
            await conn.run_sync(models.Base.metadata.create_all)

    @classmethod
    def get_db_session(cls, my_engine: engine = _db_engine):
        return async_sessionmaker(my_engine, expire_on_commit=False)


class AIOConnector(ProxyBase):

    async def save_to_db(self, val, price):
        async with super().get_db_session(self._db_engine).begin() as session:
            await session.execute(sa.insert(models.Rate).values(ticker=val, price=price, time=int(time())))
            await session.commit()


class APIConnector(ProxyBase):

    async def get_last_price(self, ticker: str):
        async with super().get_db_session().begin() as session:
            result2 = sa.select(models.Rate).where(models.Rate.ticker == ticker).order_by(
                sa.desc((sa.column('id')))).limit(1)
            last_record = await session.execute(result2)

        return last_record

    async def get_date_price(self, ticker, data: datetime.date):
        async with super().get_db_session().begin() as session:
            result2 = sa.select(models.Rate).where(models.Rate.ticker == ticker).where(
                data == sa.func.date_trunc('day', sa.func.to_timestamp(models.Rate.time)).cast(sa.Date))
            last_record = await session.execute(result2)

        return last_record

    async def get_all(self, ticker):
        async with super().get_db_session().begin() as session:
            result2 = sa.select(models.Rate).where(models.Rate.ticker == ticker).order_by((sa.column('id')))
            last_record = await session.execute(result2)

        return last_record
