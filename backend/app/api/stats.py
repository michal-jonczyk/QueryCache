from fastapi import APIRouter
from sqlalchemy import func

from core.database import SessionLocal
from core.models import QueryCache
from services.redis_service import redis_service

router = APIRouter()


@router.get("/stats")
async def get_stats():
    db = SessionLocal()

    total_queries = db.query(QueryCache).count()
    total_hits = db.query(func.sum(QueryCache.hits)).scalar() or 0

    top_queries = db.query(QueryCache).order_by(QueryCache.hits.desc()).limit(5).all()

    db.close()

    cache_info = redis_service.redis.info("memory")
    cache_size_bytes = cache_info.get("used_memory", 0)
    cache_size_kb = round(cache_size_bytes / 1024, 2)

    return {
        "total_queries": total_queries,
        "total_hits": int(total_hits),
        "cache_size": f"{cache_size_kb} KB",
        "top_queries":[
        {
            "query": q.original_query,
            "hits": q.hits,
            "cached_at": q.created_at.isoformat()
        }
            for q in top_queries
    ]
    }