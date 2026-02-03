from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.core.database import Base


class QueryCache(Base):
    __tablename__ = 'query_cache'

    id = Column(Integer, primary_key=True)
    query_hash = Column(String, unique=True, nullable=False)
    original_query = Column(String, nullable=False)
    cached_result = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    hits = Column(Integer, default=0)


class TableQueryMapping(Base):
    __tablename__ = "table_query_mapping"
    id = Column(Integer, primary_key=True)
    table_name = Column(String,nullable=False)
    query_hash = Column(String,nullable=False)
    created_at = Column(DateTime, default=datetime.now)


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    category = Column(String, nullable=False)
    stock = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)

    @property
    def price_pln(self):
        return f"{self.price / 100:.2f}"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    country = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, default=1)
    total_price = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    @property
    def price_pln(self):
        return f"{self.price / 100:.2f}"