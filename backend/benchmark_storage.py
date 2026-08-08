
# | Metric |     JSON | Parquet | Observation                |
# | ------ | -------: | ------: | -------------------------- |
# | Write  |  1.007 s | 1.168 s | JSON ~16% faster           |
# | Read   |  0.238 s | 0.537 s | JSON ~2.3× faster          |
# | Size   | 12.68 MB | 0.65 MB | **Parquet ~19.6× smaller** |
 
#  results for 100K records



from __future__ import annotations

import json
import time
from pathlib import Path

from app.storage.json_storage import JSONStorage
from app.storage.parquet_storage import ParquetStorage


DATASET_SIZE = 100_000

OUTPUT_DIR = Path("data/benchmark")


def generate_data(size: int) -> list[dict]:
    return [
        {
            "symbol": f"STOCK{i % 1000}",
            "price": 100.0 + (i % 500),
            "volume": 1000 + i,
            "sector": f"sector_{i % 10}",
        }
        for i in range(size)
    ]


def benchmark_json(data: list[dict]) -> dict:
    storage = JSONStorage()

    path = OUTPUT_DIR / "benchmark.json"

    start = time.perf_counter()

    storage.save(
        data,
        path,
    )

    write_time = time.perf_counter() - start

    start = time.perf_counter()

    storage.load(path)

    read_time = time.perf_counter() - start

    return {
        "format": "JSON",
        "write_seconds": write_time,
        "read_seconds": read_time,
        "size_bytes": path.stat().st_size,
    }


def benchmark_parquet(data: list[dict]) -> dict:
    storage = ParquetStorage()

    path = OUTPUT_DIR / "benchmark.parquet"

    start = time.perf_counter()

    storage.save(
        data,
        path,
    )

    write_time = time.perf_counter() - start

    start = time.perf_counter()

    storage.load(path)

    read_time = time.perf_counter() - start

    return {
        "format": "Parquet",
        "write_seconds": write_time,
        "read_seconds": read_time,
        "size_bytes": path.stat().st_size,
    }


def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(
        f"Generating {DATASET_SIZE:,} records..."
    )

    data = generate_data(
        DATASET_SIZE
    )

    json_result = benchmark_json(data)

    parquet_result = benchmark_parquet(data)

    print("\nBenchmark Results")
    print("=" * 60)

    for result in [
        json_result,
        parquet_result,
    ]:
        print(
            f"\n{result['format']}"
        )

        print(
            f"Write : "
            f"{result['write_seconds']:.4f} sec"
        )

        print(
            f"Read  : "
            f"{result['read_seconds']:.4f} sec"
        )

        print(
            f"Size  : "
            f"{result['size_bytes']:,} bytes"
        )


if __name__ == "__main__":
    main()

 
 