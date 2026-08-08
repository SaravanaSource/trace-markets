from __future__ import annotations

from pathlib import Path
from typing import Any

import duckdb

from app.query.base_query_engine import BaseQueryEngine


class DuckDBEngine(BaseQueryEngine):
    """
    DuckDB implementation of the analytical query engine.
    """

    def __init__(
        self,
        database: str | Path = ":memory:",
    ):
        self.database = str(database)

    def query(
        self,
        sql: str,
    ) -> Any:
        """
        Execute SQL using DuckDB.
        """

        with duckdb.connect(
            self.database
        ) as connection:

            return connection.sql(sql).fetchall()
