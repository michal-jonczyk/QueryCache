from fastapi import FastAPI
from datetime import datetime

from api.query import router as query_router
from api.stats import router as stats_router
from api.cache import router as cache_router
from core.config import settings
from core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="Intelligent SQL query caching middleware with Redis",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)


app.include_router(cache_router)
app.include_router(stats_router)
app.include_router(query_router)

@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "message": "Welcome! Check /docs for API documentation."
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "querycache",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)