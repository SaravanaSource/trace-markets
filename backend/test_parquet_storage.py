from pathlib import Path

from app.storage.parquet_storage import ParquetStorage


def main():

    storage = ParquetStorage()

    data = [
        {
            "symbol": "INFY",
            "price": 1850.25,
            "volume": 500000,
        },
        {
            "symbol": "TCS",
            "price": 3200.50,
            "volume": 300000,
        },
    ]

    path = Path("data/test/stocks.parquet")

    storage.save(
        data,
        path,
    )

    result = storage.load(path)

    print(result)


if __name__ == "__main__":
    main()
