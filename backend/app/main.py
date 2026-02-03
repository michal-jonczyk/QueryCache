from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import query, stats, cache, invalidate

app = FastAPI(
    title="QueryCache API",
    description="SQL Query Caching Middleware with Redis",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://query-cache.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(query.router, tags=["Query"])
app.include_router(stats.router, tags=["Statistics"])
app.include_router(cache.router, tags=["Cache"])
app.include_router(invalidate.router, tags=["Invalidation"])


@app.get("/")
async def root():
    return {
        "message": "QueryCache API is running",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.on_event("startup")
async def startup_event():
    """Seed database on startup if empty"""
    from app.core.seed_database import seed_database
    from app.core.database import SessionLocal
    from app.core.models import Product

    db = SessionLocal()
    try:
        # Check if database is empty
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


@app.get("/seed-now")
async def manual_seed():
    """Manual database seeding"""
    from app.core.seed_database import seed_database
    from app.core.database import SessionLocal
    from app.core.models import Product

    db = SessionLocal()
    try:
        count_before = db.query(Product).count()
        print(f"Products before seeding: {count_before}")

        seed_database()

        count_after = db.query(Product).count()
        print(f"Products after seeding: {count_after}")

        return {
            "status": "success",
            "products_before": count_before,
            "products_after": count_after
        }
    except Exception as e:
        print(f"ERROR: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)