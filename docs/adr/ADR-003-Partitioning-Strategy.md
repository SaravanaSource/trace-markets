# ADR-003: Bronze Data Lake Partitioning Strategy

**Status:** Accepted

**Date:** 2026-08-02

**Epic:** Epic 3 – Data Lake Engineering

**Sprint:** Sprint 10 – Professional Bronze Layer

---

# Context

Trace Markets is being designed as a production-grade Financial Data Platform.

The Bronze layer is responsible for storing immutable raw data collected from multiple external systems such as:

- NSE
- BSE
- RBI
- SEBI
- News Providers
- Mutual Funds
- ETFs
- Corporate Actions
- Options
- Futures

As the platform grows, the data volume is expected to increase significantly.

Future scale targets:

- 5,000+ securities
- 20+ years of historical data
- Minute-level market data
- Tick data (future)
- News streams
- Real-time ingestion
- Apache Spark processing
- Apache Iceberg
- DuckDB
- PostgreSQL
- Kafka

The physical storage layout chosen today must continue to work when the dataset grows to billions of records.

---

# Problem Statement

How should Bronze files be physically organized inside the Data Lake?

The partition strategy directly affects:

- Query performance
- Storage efficiency
- Spark performance
- Iceberg compatibility
- Cost
- Future scalability
- Maintenance

A poor partition strategy can significantly degrade performance as the platform grows.

---

# Design Goals

The partitioning strategy should:

- Support future big data workloads.
- Minimize unnecessary file scanning.
- Support Spark partition pruning.
- Support Iceberg migration.
- Scale to billions of records.
- Remain understandable.
- Avoid excessive folder creation.

---

# Options Considered

---

## Option A

```
bronze/

source/

date/
```

Example

```
bronze/

nse/

2026-08-02/
```

### Advantages

- Simple
- Easy to understand

### Disadvantages

- Date is not query-friendly.
- Does not follow Hive partition conventions.
- Harder for Spark to optimize.

---

## Option B

```
bronze/

symbol/

year/

month/

day/
```

Example

```
bronze/

INFY/

2026/

08/

02/
```

### Advantages

Easy to locate one stock manually.

### Disadvantages

Very high cardinality.

Future estimate:

```
5,000 symbols

×

20 years

=

Millions of folders
```

Spark performs poorly with excessive partitions.

Folder explosion.

Rejected.

---

## Option C (Selected)

```
bronze/

source=nse/

market=equity/

year=2026/

month=08/

day=02/
```

Example

```
bronze/

source=nse/

market=equity/

year=2026/

month=08/

day=02/

part-000001.json
```

### Advantages

- Hive compatible
- Spark partition pruning
- Iceberg compatible
- Easy archival
- Time-series friendly
- Low partition cardinality
- Easy filtering by source and market

### Disadvantages

Finding a single symbol requires filtering after reading the partition.

However, Spark is optimized for this use case.

---

# Cardinality Analysis

## Low Cardinality

Good partition columns.

Examples

```
Source

NSE
BSE
RBI
SEBI
```

```
Market

Equity
ETF
Options
Futures
Commodity
Currency
```

```
Year

2025

2026

2027
```

---

## High Cardinality

Poor partition columns.

Examples

```
Stock Symbol

INFY

TCS

RELIANCE

HDFCBANK

5000+ values
```

```
ISIN

Every company has a unique ISIN.
```

```
Trade ID

Millions of unique values.
```

High-cardinality partitions create millions of directories and small files.

---

# Why Symbol is NOT a Partition

Initially, partitioning by stock symbol appears intuitive.

However, in large-scale systems it causes:

- Folder explosion
- Millions of partitions
- Small file problem
- Slow metadata operations
- Poor Spark planning

Instead, symbol remains a normal data column inside the Bronze record.

Spark filters symbols after reading the required date partitions.

---

# Expected Query Patterns

Typical analytics queries include:

```
Load today's NSE data.

Load yesterday's options.

Load all equity data for August 2026.

Load RBI data for this month.
```

These queries naturally align with:

```
Source

↓

Market

↓

Date
```

rather than individual symbols.

---

# Future Compatibility

This design is compatible with:

- Apache Spark
- Apache Hive
- Apache Iceberg
- Delta Lake
- DuckDB
- Trino
- Presto

No structural migration should be required.

---

# Trade-offs

| Decision | Benefit | Cost |
|-----------|----------|------|
| Partition by Source | Easy filtering | One additional folder level |
| Partition by Market | Supports multiple asset classes | Slightly deeper hierarchy |
| Partition by Date | Excellent time-series performance | Queries by symbol require filtering |
| Avoid Symbol Partition | Prevents folder explosion | Requires Spark filtering |

---

# Final Decision

Trace Markets will use the following Bronze layout:

```
bronze/

source=<source>/

market=<market>/

year=<yyyy>/

month=<mm>/

day=<dd>/

part-000001.json
```

Example

```
bronze/

source=nse/

market=equity/

year=2026/

month=08/

day=02/

part-000001.json
```

---

# Future Evolution

Later versions may introduce:

- hour=<hh>
- minute=<mm>
- Iceberg hidden partitioning
- Parquet storage
- Manifest files
- Metadata catalogs
- Automatic compaction
- Small file optimization

---

# Consequences

This decision provides:

- Production-grade partitioning
- Excellent Spark compatibility
- Future Iceberg migration
- Efficient time-series analytics
- Low operational complexity
- Scalable storage organization

This ADR establishes the long-term physical layout of the Bronze Data Lake for Trace Markets.
