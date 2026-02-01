from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from core.database import Base


class QueryCache(Base):
    __tablename__ = 'query_cache'

    id = Column(Integer, primary_key=True)
    query_hash = Column(String, unique=True, nullable=False)
    original_query = Column(String, nullable=False)
    cached_result = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    hits = Column(Integer, default=0)