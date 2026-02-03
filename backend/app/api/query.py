import hashlib
import json

from fastapi import APIRouter
from datetime import datetime

from core.database import SessionLocal
from core.models import QueryCache
from services.redis_service import redis_service
from services.normalizer import normalize_query
from services.sql_parser import get_query_type, extract_tables

router = APIRouter()


@router.get("/parse")
async def parse_query(sql: str):
    return {
        "query": sql,
        "type": get_query_type(sql),
        "tables": extract_tables(sql)
    }


@router.get("/query")
async def execute_query(sql: str):
    normalized_sql = normalize_query(sql)
    query_hash = hashlib.md5(normalized_sql.encode()).hexdigest()

    cached = await redis_service.get(query_hash)
    if cached:
        db = SessionLocal()
        cache_entry = db.query(QueryCache).filter(
            QueryCache.query_hash == query_hash
        ).first()

        if cache_entry:
            cache_entry.hits += 1
            db.commit()
        db.close()

        return {
            "source": "cache",
            "query": sql,
            "result": json.loads(cached),
            "cached_at": datetime.now().isoformat()
        }

    simulated_result = {"rows": [{"id": 1, "name": "Product 1"}, {"id": 2, "name": "Product 2"}]}

    await redis_service.set(query_hash, json.dumps(simulated_result))

    db = SessionLocal()
    cache_entry = db.query(QueryCache).filter(
        QueryCache.query_hash == query_hash
    ).first()

    if not cache_entry:
        cache_entry = QueryCache(
            query_hash=query_hash,
            original_query=sql,
            cached_result=json.dumps(simulated_result),
        )
        db.add(cache_entry)
        db.commit()
    db.close()

    return {
        "source": "database",
        "query": sql,
        "result": simulated_result,
        "cached_at": datetime.now().isoformat()
    }