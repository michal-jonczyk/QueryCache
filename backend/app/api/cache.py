from fastapi import APIRouter

from app.core.database import SessionLocal
from app.core.models import QueryCache
from app.services.redis_service import redis_service

router = APIRouter()

@router.delete("/cache")
async def clear_cache(clear_db:bool = False):
    redis_keys_deleted = 0

    for key in redis_service.redis.keys("*"):
        redis_service.redis.delete(key)
        redis_keys_deleted += 1

    db_records_deleted = 0
    if clear_db:
        db = SessionLocal()
        db_records_deleted = db.query(QueryCache).delete()
        db.commit()
        db.close()

    return {
        "message": "Cache cleared successfully",
        "redis_keys_deleted": redis_keys_deleted,
        "db_records_deleted": db_records_deleted
    }