import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["app"] == "QueryCache"
    assert response.json()["status"] == "running"


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_stats_endpoint():
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_queries" in data
    assert "total_hits" in data
    assert "cache_size" in data
    assert "top_queries" in data


def test_query_endpoint():
    response = client.get("/query?sql=SELECT * FROM test")
    assert response.status_code == 200
    data = response.json()
    assert "source" in data
    assert "query" in data
    assert "result" in data


def test_query_caching():
    sql = "SELECT * FROM test_cache WHERE id=999"

    response1 = client.get(f"/query?sql={sql}")
    assert response1.status_code == 200
    assert response1.json()["source"] == "database"

    response2 = client.get(f"/query?sql={sql}")
    assert response2.status_code == 200
    assert response2.json()["source"] == "cache"


def test_query_normalization():
    sql1 = "SELECT * FROM products WHERE id=1"
    sql2 = "SELECT  *  FROM  products  WHERE  id=1"

    response1 = client.get(f"/query?sql={sql1}")
    assert response1.status_code == 200

    response2 = client.get(f"/query?sql={sql2}")
    assert response2.status_code == 200
    assert response2.json()["source"] == "cache"


def test_invalidate_update_query():
    response = client.post("/invalidate?sql=UPDATE products SET price=100 WHERE id=1")
    assert response.status_code == 200
    data = response.json()
    assert data["query_type"] == "UPDATE"
    assert "products" in data["tables"]


def test_invalidate_select_query_rejected():
    response = client.post("/invalidate?sql=SELECT * FROM products")
    assert response.status_code == 200
    data = response.json()
    assert "Only UPDATE/INSERT/DELETE" in data["message"]


def test_parse_endpoint():
    response = client.get("/parse?sql=SELECT * FROM users WHERE id=1")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "SELECT"
    assert "users" in data["tables"]


def test_cache_clear():
    response = client.delete("/cache?clear_db=false")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "redis_keys_deleted" in data