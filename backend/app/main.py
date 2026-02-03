from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from app.api.query import router as query_router
from app.api.stats import router as stats_router
from app.api.cache import router as cache_router
from app.core.config import settings
from app.core.database import Base, engine
from app.api.invalidate import router as invalidate_router
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="Intelligent SQL query caching middleware with Redis",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
        "https://query-cache.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(cache_router)
app.include_router(stats_router)
app.include_router(query_router)
app.include_router(invalidate_router)

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


@app.on_event("startup")
async def startup_event():
    """Seed database on startup if empty"""
    from app.core.seed_database import seed_database
    from app.core.database import SessionLocal
    from app.core.models import Product

    db = SessionLocal()
    try:
        product_count = db.query(Product).count()
        if product_count == 0:
            print("📦 Database is empty, seeding...")
            seed_database()
            print("✅ Database seeded successfully!")
        else:
            print(f"✅ Database already has {product_count} products")
    except Exception as e:
        print(f"⚠️ Seeding check failed: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)