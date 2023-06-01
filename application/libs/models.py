from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .db import Db


Base = declarative_base()
Base.query = Db.static().get_session().query_property()


class Config(Base):
    __tablename__ = 'configs'

    id: Mapped[int] = Column(Integer, primary_key=True)
    key: Mapped[str] = Column(String, unique=True)
    value: Mapped[Optional[str]] = Column(String)

    def __repr__(self) -> str:
        return f"Config(id={self.id!r}, key={self.key!r})"


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String, unique=True)
    token: Mapped[str] = Column(String)
    deleted: Mapped[Optional[str]] = Column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = Column(Integer, primary_key=True)
    uuid: Mapped[str] = Column(String, unique=True)
    name: Mapped[str] = Column(String)
    desc: Mapped[str] = Column(String)
    deleted: Mapped[Optional[str]] = Column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"Product(id={self.id!r}, name={self.name!r}, desc={self.desc!r})"


class ProductOffer(Base):
    __tablename__ = 'product_offers'

    id: Mapped[int] = Column(Integer, primary_key=True)
    product_id: Mapped[int] = Column(Integer, ForeignKey("products.id"))
    price: Mapped[int] = Column(Integer)
    pieces: Mapped[int] = Column(Integer)
    added: Mapped[str] = Column(DateTime)

    product: Mapped["Product"] = relationship('Product', foreign_keys=[product_id])

    def __repr__(self) -> str:
        return f"ProductOffer(id={self.id!r}, product={self.product_id!r}, added={self.added!r})"
