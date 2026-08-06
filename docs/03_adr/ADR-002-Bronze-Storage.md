# ADR-002: Bronze Storage

**Status:** Accepted

**Date:** 2026-08-01

## Context
Trace Markets follows the Bronze → Silver → Gold architecture.
Raw data must be preserved exactly as received.

## Problem
Should ingestion classes write files directly?

## Decision
Create a dedicated `BronzeStorage` service responsible only for persistence.

## Trace Markets Architecture

```text
APIIngestion
      │
      ▼
BronzeStorage
      │
      ▼
Bronze Data Lake
```

The ingestion framework decides **what** to save.
BronzeStorage decides **how** to save it.

## Benefits
- Separation of concerns
- Storage independence
- Future support for S3, Azure Blob, Iceberg
- Easier testing

## OOP
- Composition
- Encapsulation
- Abstraction

## SOLID
- SRP
- OCP

## Production Example
Databricks, Snowflake, Delta Lake and cloud data platforms preserve immutable raw data before transformation.

## Future Evolution
- Metadata
- Partitioning
- Parquet
- Schema versioning
- Manifest files
- Iceberg integration

## Consequences
Provides the foundation for the entire Trace Markets Data Lake.
