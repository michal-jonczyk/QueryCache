import re
from typing import List,Optional


def get_query_type(sql:str) -> str:
    sql_upper = sql.upper().strip()

    if sql_upper.startswith("SELECT"):
        return "SELECT"
    elif sql_upper.startswith("INSERT"):
        return "INSERT"
    elif sql_upper.startswith("UPDATE"):
        return "UPDATE"
    elif sql_upper.startswith("DELETE"):
        return "DELETE"
    else:
        return "UNKNOWN"


def extract_tables(sql:str) -> List[str]:
    sql_lower = sql.lower()
    tables = []

    from_pattern = r'\bfrom\s+([a-z_][a-z0-9_]*)'
    from_matches = re.findall(from_pattern, sql_lower)
    tables.extend(from_matches)

    join_pattern = r'\bjoin\s+([a-z_][a-z0-9_]*)'
    join_matches = re.findall(join_pattern, sql_lower)
    tables.extend(join_matches)

    update_pattern = r'\bupdate\s+([a-z_][a-z0-9_]*)'
    update_matches = re.findall(update_pattern, sql_lower)
    tables.extend(update_matches)

    insert_pattern = r'\binsert\s+into\s+([a-z_][a-z0-9_]*)'
    insert_matches = re.findall(insert_pattern, sql_lower)
    tables.extend(insert_matches)

    delete_pattern = r'\bdelete\s+from\s+([a-z_][a-z0-9_]*)'
    delete_matches = re.findall(delete_pattern, sql_lower)
    tables.extend(delete_matches)

    return list(set(tables))