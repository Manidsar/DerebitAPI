from sqlalchemy import String, Float, Integer
from sqlalchemy import orm


Base = orm.declarative_base()


class Rate(Base):
    __tablename__ = 'currency_price'
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    ticker: orm.Mapped[str] = orm.mapped_column(String(30))
    price: orm.Mapped[float] = orm.mapped_column(Float)
    time: orm.Mapped[int] = orm.mapped_column(Integer)
