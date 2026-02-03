from fastapi import APIRouter

from app.core.database import SessionLocal
from app.core.models import QueryCache, TableQueryMapping
from app.services.redis_service import redis_service
from app.services.sql_parser import get_query_type, extract_tables

router = APIRouter()


@router.post("/invalidate")
async def invalidate_cache(sql:str):
    query_type = get_query_type(sql)

    if query_type not in ["UPDATE","INSERT","DELETE"]:
        return {
            "message": "Only UPDATE/INSERT/DELETE queries trigger invalidation",
            "query_type": query_type
        }

    tables = extract_tables(sql)

    if not tables:
        return {
            "message": "No tables detected in query",
            "tables": []
        }

    db = SessionLocal()
    invalidated_count = 0

    for table in tables:
        mappings = db.query(TableQueryMapping).filter(
            TableQueryMapping.table_name == table
        ).all()

        for mapping in mappings:
            await redis_service.delete(mapping.query_hash)
            invalidated_count += 1

    db.close()


    return {
        "message": "Cache invalidated successfully",
        "query_type": query_type,
        "tables": tables,
        "cache_keys_invalidated": invalidated_count
    }