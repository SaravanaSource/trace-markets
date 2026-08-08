from app.query.duckdb_engine import DuckDBEngine


def main():

    engine = DuckDBEngine()

    result = engine.query(
        """
        SELECT
            symbol,
            price
        FROM read_parquet(
            'data/benchmark/benchmark.parquet'
        )
        WHERE sector = 'sector_5'
        LIMIT 10
        """
    )

    print(result)


if __name__ == "__main__":
    main()
