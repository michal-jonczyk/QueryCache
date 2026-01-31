# ⚡ QueryCache

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7.0-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?style=for-the-badge)

**Intelligent SQL query caching middleware with Redis + FastAPI**

🚧 **Work in Progress** - Building in public (February 2025)

</div>

---

## 🎯 What Problem Does This Solve?

Database queries are slow. Repeated identical queries waste time and resources.

**QueryCache fixes this:**
- ✅ First query: ~200ms (hits database)
- ✅ Cached query: ~2ms (hits Redis)
- ✅ 99% response time reduction

---

## ✨ Key Features (Planned)

- 🔗 **Smart SQL Caching** - Automatic query result caching
- ⚡ **Redis Backend** - Lightning-fast in-memory storage
- 🤖 **AI-Powered Invalidation** - Smart cache clearing (Week 2)
- 📊 **Performance Dashboard** - Real-time cache hit/miss stats
- 🔄 **Query Normalization** - `SELECT * WHERE id=1` = `SELECT * WHERE id=2` pattern

---

## 🛠️ Tech Stack

**Backend:**
- **FastAPI** - Modern async Python framework
- **Redis** - In-memory data store
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation

**Frontend:**
- **React** - UI library
- **Tailwind CSS** - Styling
- **Recharts** - Performance visualization

---

## 📅 Development Timeline

**Week 1 (Feb 3-9):** Setup + Basic Caching  
**Week 2 (Feb 10-16):** SQL Normalization + AI Invalidation  
**Week 3 (Feb 17-23):** Dashboard + Tests + Deploy  

---

## 🚀 Quick Start (Coming Soon)
```bash
# Clone repository
git clone https://github.com/michal-jonczyk/QueryCache.git

# Backend setup
cd QueryCache/backend
pip install -r requirements.txt

# Run Redis (Docker)
docker run -d -p 6379:6379 redis:7

# Start server
uvicorn app.main:app --reload
```

---

## 📖 Documentation

Full documentation coming soon!

---

## 👨‍💻 Author

**Michał Jończyk**
- GitHub: [@michal-jonczyk](https://github.com/michal-jonczyk)

---

## 📝 License

MIT License

---

<div align="center">

**⭐ Star this repo if you find it interesting!**

*Building in public - Follow the journey*

</div>