# ⚡ QueryCache

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7.0-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Tailwind](https://img.shields.io/badge/Tailwind-4.0-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

**Intelligent SQL query caching middleware with Redis + FastAPI**

</div>

---

## 📸 Screenshots

### Dashboard - Database Query (First Request)
![Database Query](screenshots/query-cache-database.webp)
*Initial query execution from database: 22.36ms*

### Dashboard - Cached Query (Subsequent Requests)
![Cached Query](screenshots/query-cache-cache.webp)
*Same query served from Redis cache: 2ms (11x faster!)*

### Real-time Statistics & Analytics
![Statistics](screenshots/query-cache-top.webp)
*Track query performance, cache hits, and most frequently accessed queries*

---

## 💡 Try it live: [query-cache.vercel.app](https://query-cache.vercel.app)

---

## 🎯 What Problem Does This Solve?

Database queries are slow and wasteful:

❌ Repeated identical queries waste resources  
❌ ~200ms response times for simple SELECTs  
❌ Database overload from redundant requests  

**QueryCache fixes this:**

✅ First query: ~20ms (hits database)  
✅ Cached query: ~2ms (hits Redis)  
✅ **90% response time reduction**  

---

## ✨ Key Features

### 🚀 **Automatic Query Caching**
Execute any SELECT query - results are automatically cached in Redis.
```sql
SELECT * FROM products WHERE category = 'Electronics'
```
- First call: Database (~20ms)
- Subsequent calls: Redis cache (~2ms)

### ⚡ **Smart Cache Invalidation**
Cache automatically invalidates when data changes:
```sql
UPDATE products SET price = 999 WHERE id = 1
```
→ All cached queries involving `products` table are cleared

### 📊 **Real-time Dashboard**
- Live cache hit/miss statistics
- Top cached queries ranking
- Cache size monitoring
- Auto-refresh every 5 seconds

### 🔍 **Query Normalization**
Smart pattern recognition treats similar queries identically:
```sql
SELECT * FROM users WHERE id = 1
SELECT * FROM users WHERE id = 2
```
→ Both use the same cache pattern

### 🎨 **Interactive Playground**
- Execute queries directly from browser
- Real-time execution time comparison
- Source indicator (DATABASE vs CACHE)
- One-click cache clearing

---

## 🛠️ Tech Stack

**Backend:**

- **FastAPI** - Modern async Python framework
- **Redis** - In-memory caching layer
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite** - Development database (easily swappable)
- **Pydantic** - Data validation
- **Railway** - Backend deployment

**Frontend:**

- **React 19** - UI library with hooks
- **Tailwind CSS** - Utility-first styling
- **Vite** - Lightning-fast build tool
- **Vercel** - Frontend deployment

---

## ⚡ Installation

### Prerequisites
```bash
# Python 3.11+ required
python --version

# Node.js 20+ for frontend
node --version
```

---

## 🔧 Backend Setup
```bash
# 1. Clone repository
git clone https://github.com/michal-jonczyk/query-cache.git
cd query-cache/backend

# 2. Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start Redis (Docker)
docker run -d -p 6379:6379 redis:7

# Alternative: Use local Redis installation
# redis-server

# 5. Configure environment
cd app
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# 6. Seed database (optional - adds sample data)
python core/seed_database.py

# 7. Run backend
uvicorn main:app --reload

# ✅ Backend: http://localhost:8000
# 📖 API docs: http://localhost:8000/docs
```

Your `.env` should contain:
```env
APP_NAME=QueryCache
APP_VERSION=0.1.0
PORT=8000
BASE_URL=http://localhost:8000

REDIS_HOST=localhost
REDIS_PORT=6379

DATABASE_URL=sqlite:///./querycache.db
```

---

## 🎨 Frontend Setup
```bash
# New terminal
cd query-cache/frontend

# 1. Install dependencies
npm install

# 2. Run dev server
npm run dev

# ✅ Frontend: http://localhost:5173
```

---

## 🧪 Test the Setup

### 1. Check Backend Health
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-03T15:30:00",
  "service": "querycache"
}
```

### 2. Execute a Query
```bash
curl -X GET "http://localhost:8000/query?sql=SELECT%20*%20FROM%20products%20LIMIT%205"
```

### 3. View Statistics
```bash
curl http://localhost:8000/stats
```

Expected response:
```json
{
  "total_queries": 1,
  "total_hits": 0,
  "cache_size": "1.2 KB",
  "top_queries": [...]
}
```

---

## 🏗️ Project Architecture
```
query-cache/
├── backend/
│   └── app/
│       ├── api/
│       │   ├── query.py         # Query execution + caching
│       │   ├── stats.py         # Statistics endpoint
│       │   ├── cache.py         # Cache management
│       │   └── invalidate.py    # Smart invalidation
│       │
│       ├── services/
│       │   ├── redis_service.py    # Redis client wrapper
│       │   ├── normalizer.py       # Query normalization
│       │   └── sql_parser.py       # Table extraction
│       │
│       ├── core/
│       │   ├── config.py           # Settings management
│       │   ├── database.py         # SQLAlchemy setup
│       │   ├── models.py           # DB models
│       │   └── seed_database.py    # Sample data
│       │
│       └── main.py                 # FastAPI app
│
└── frontend/
    └── src/
        ├── App.jsx                 # Main dashboard
        ├── QueryPlayground.jsx     # Interactive query UI
        └── main.jsx
```

---

## 🔄 Request Flow

### 1. **Query Execution**
```
User → POST /query?sql=SELECT * FROM products
     → Normalize query (lowercase, trim spaces)
     → Generate MD5 hash
     → Check Redis cache
```

### 2. **Cache Hit**
```
Redis has data
→ Increment hit counter in SQLite
→ Return cached result (~2ms)
```

### 3. **Cache Miss**
```
Redis has no data
→ Execute query on SQLite (~200ms)
→ Store result in Redis (TTL: 5 minutes)
→ Store mapping: table → query_hash
→ Return fresh result
```

### 4. **Smart Invalidation**
```
User → POST /invalidate?sql=UPDATE products SET price=100
     → Parse query type (UPDATE/INSERT/DELETE)
     → Extract affected tables
     → Find all cached queries for those tables
     → Delete from Redis
```

---

## 💡 What I Learned

### Technical Challenges Solved

#### 1️⃣ **Cache Invalidation Strategy**

**Problem:** How to know which cached queries to invalidate when data changes?

**Solution:** Table-Query mapping in SQLite:
```python
class TableQueryMapping(Base):
    __tablename__ = "table_query_mapping"
    id = Column(Integer, primary_key=True)
    table_name = Column(String, nullable=False)
    query_hash = Column(String, nullable=False)
```

When a query is cached, we extract all tables it references:
```python
tables = extract_tables("SELECT * FROM products JOIN users")
# → ["products", "users"]

for table in tables:
    mapping = TableQueryMapping(
        table_name=table,
        query_hash=query_hash
    )
    db.add(mapping)
```

When data changes:
```python
affected_tables = extract_tables("UPDATE products SET price=100")
# → ["products"]

for table in affected_tables:
    mappings = db.query(TableQueryMapping).filter_by(table_name=table).all()
    for mapping in mappings:
        redis_service.delete(mapping.query_hash)
```

**Key Takeaway:** Relational databases can support cache invalidation logic elegantly.

---

#### 2️⃣ **Query Normalization**

**Problem:** `SELECT * FROM users WHERE id=1` and `SELECT  *  FROM  users  WHERE  id=1` are identical but hash differently.

**Solution:** Normalize before hashing:
```python
def normalize_query(sql: str) -> str:
    sql = sql.lower()           # Case-insensitive
    sql = sql.strip()           # Remove leading/trailing spaces
    sql = re.sub(r"\s+", " ", sql)  # Collapse multiple spaces
    return sql
```

**Key Takeaway:** String normalization is critical for cache key generation.

---

#### 3️⃣ **Redis Connection on Railway**

**Problem:** `REDIS_HOST` and `REDIS_PORT` work locally but fail on Railway.

**Solution:** Use `REDIS_URL` with automatic fallback:
```python
class RedisService:
    def __init__(self):
        redis_url = os.getenv('REDIS_URL')
        
        if redis_url:
            self.redis = redis.from_url(redis_url, decode_responses=True)
        else:
            self.redis = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                decode_responses=True,
            )
```

**Key Takeaway:** Cloud platforms use connection strings, not separate host/port.

---

#### 4️⃣ **SQLite for Prototyping**

**Problem:** PostgreSQL overkill for learning project, but need relational features.

**Solution:** SQLite with SQLAlchemy ORM - easily swappable:
```python
# Development (SQLite)
DATABASE_URL = "sqlite:///./querycache.db"

# Production (PostgreSQL) - just change this:
DATABASE_URL = "postgresql://user:pass@host:5432/db"
```

**Key Takeaway:** SQLAlchemy abstracts database differences perfectly.

---

#### 5️⃣ **Import Path Issues on Railway**

**Problem:** Local imports worked (`from api.query import ...`) but failed on Railway with `ModuleNotFoundError`.

**Solution:** Use absolute imports with package prefix:
```python
# ❌ Local only
from api.query import router

# ✅ Works everywhere
from app.api.query import router
```

Plus add `__init__.py` files in every package directory.

**Key Takeaway:** Deployment environments are strict about Python package structure.

---

### Skills Developed

✅ **Caching Strategies** - TTL, invalidation, hit/miss tracking  
✅ **SQL Parsing** - Regex-based table extraction, query classification  
✅ **Redis Integration** - Client management, connection handling  
✅ **FastAPI** - Async endpoints, CORS, dependency injection  
✅ **React Hooks** - useState, useEffect with intervals  
✅ **Deployment** - Railway (backend), Vercel (frontend), environment variables  

---

## 🔮 Future Improvements

### Planned Features

- [ ] **PostgreSQL Support** - Replace SQLite for production
- [ ] **Cache Analytics** - Graphs showing hit rates over time (Recharts)
- [ ] **Query Explain** - Show execution plans for slow queries
- [ ] **Custom TTL** - User-defined cache expiration per query
- [ ] **Webhook Notifications** - Alert when cache hit rate drops
- [ ] **Query Templates** - Save and reuse common queries
- [ ] **User Authentication** - Personal dashboards with saved queries

### Nice to Have

- [ ] **Database Adapter** - Support MySQL, MongoDB, etc.
- [ ] **Distributed Cache** - Redis Cluster for horizontal scaling
- [ ] **Query Optimizer** - Suggest indexes for frequently cached queries
- [ ] **A/B Testing** - Compare cache vs no-cache performance
- [ ] **Export Data** - Download stats as CSV/JSON
- [ ] **Docker Compose** - One-command local setup

> 💭 **Note:** This is a learning/portfolio project. These features would make it production-ready.

---

## 🚀 Deployment

### Backend (Railway)

1. Create account at [Railway.app](https://railway.app)
2. Connect GitHub repository
3. Add **Redis** database to project
4. Set environment variables:
```env
   REDIS_URL=${{ Redis.REDIS_URL }}
   DATABASE_URL=sqlite:///./querycache.db
```
5. Set **Root Directory** to `backend`
6. Deploy from `main` branch

### Frontend (Vercel)

1. Update API URL in `frontend/src/App.jsx` and `QueryPlayground.jsx`:
```javascript
   const API_URL = 'https://querycache-production.up.railway.app'
```

2. Deploy to Vercel:
```bash
   cd frontend
   npm run build
   vercel --prod
```

3. Add environment variable in Vercel:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://querycache-production.up.railway.app`

4. Update CORS in backend `main.py`:
```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "http://localhost:5173",
           "https://query-cache.vercel.app",  # Your Vercel URL
       ],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 🤝 Contributing

This is a portfolio project, but suggestions welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push (`git push origin feature/amazing`)
5. Open Pull Request

---

## 👨‍💻 Author

**Michał Jończyk**

- GitHub: [@michal-jonczyk](https://github.com/michal-jonczyk)

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python framework
- [Redis](https://redis.io/) - In-memory data store
- [Railway](https://railway.app/) - Simple deployment platform
- [Vercel](https://vercel.com/) - Frontend hosting

---

## 🚀 Live Demo

- **Dashboard**: [https://query-cache.vercel.app](https://query-cache.vercel.app)
- **API Documentation**: [https://querycache-production.up.railway.app/docs](https://querycache-production.up.railway.app/docs)

Try executing SQL queries and see the caching in action! First query hits the database (~200ms), subsequent queries hit Redis cache (~2ms). **99% faster!** ⚡