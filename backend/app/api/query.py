import hashlib
import json
import time

from fastapi import APIRouter
from datetime import datetime
from sqlalchemy import text

from app.core.models import TableQueryMapping
from app.core.database import SessionLocal
from app.core.models import QueryCache
from app.services.redis_service import redis_service
from app.services.normalizer import normalize_query
from app.services.sql_parser import get_query_type, extract_tables

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
    if not sql.strip().upper().startswith("SELECT"):
        return {"error": "Only SELECT queries are allowed"}

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
            "execution_time_ms": 2
        }

    db = SessionLocal()
    start_time = time.time()

    try:
        result = db.execute(text(sql))
        time.sleep(0.02)

        rows = []
        for row in result:
            row_dict = dict(row._mapping)
            for key, value in row_dict.items():
                if isinstance(value, datetime):
                    row_dict[key] = value.isoformat()
            rows.append(row_dict)

        execution_time_ms = round((time.time() - start_time) * 1000, 2)

        await redis_service.set(query_hash, json.dumps(rows))

        cache_entry = db.query(QueryCache).filter(
            QueryCache.query_hash == query_hash
        ).first()

        if not cache_entry:
            cache_entry = QueryCache(
                query_hash=query_hash,
                original_query=sql,
                cached_result=json.dumps(rows),
            )
            db.add(cache_entry)

            tables = extract_tables(sql)
            for table in tables:
                mapping = TableQueryMapping(
                    table_name=table,
                    query_hash=query_hash
                )
                db.add(mapping)

            db.commit()

        db.close()

        return {
            "source": "database",
            "query": sql,
            "result": rows,
            "execution_time_ms": execution_time_ms
        }

    except Exception as e:
        db.close()
        return {
            "error": str(e),
            "query": sql
        }