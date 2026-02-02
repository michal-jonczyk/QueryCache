import re


def normalize_query(sql: str) -> str:
    sql = sql.lower()
    sql = sql.strip()
    sql = re.sub(r"\s+", " ", sql)
    return sql

