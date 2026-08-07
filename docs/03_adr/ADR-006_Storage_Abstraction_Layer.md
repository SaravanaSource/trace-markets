# ADR-006: Storage Abstraction Layer

**Status:** Accepted\
**Date:** 2026-08-07\
**Epic:** EDR-005 -- Analytical Storage Engine

------------------------------------------------------------------------

# Context

Trace Markets currently persists Bronze data directly as JSON through
`BronzeStorage`.

Current flow:

``` text
API
    ↓
BaseIngestion
    ↓
BronzeStorage
    ↓
json.dump()
```

This tightly couples business logic with a specific storage technology.

Future roadmap includes JSON, Parquet, DuckDB, Apache Iceberg, and Delta
Lake.

------------------------------------------------------------------------

# Problem Statement

Business logic should request **storage**, not **JSON**.

We need an architecture where:

-   Business logic requests storage.
-   Storage implementations decide how persistence happens.

------------------------------------------------------------------------

# Decision Drivers

-   Maintainability
-   Extensibility
-   Low coupling
-   Testability
-   Future migration
-   Alignment with Trace Core vision

------------------------------------------------------------------------

# Considered Options

## Option 1 -- Direct JSON Usage

``` text
BronzeStorage
    ↓
json.dump()
```

**Pros**

-   Very simple

**Cons**

-   Tight coupling
-   Difficult migration
-   Poor testability

**Decision:** Rejected.

------------------------------------------------------------------------

## Option 2 -- Storage Abstraction (Chosen)

``` text
BaseStorage
      ▲
      │
JSONStorage
ParquetStorage
IcebergStorage
```

**Pros**

-   Low coupling
-   Technology independent
-   Easy migration
-   Easy testing

**Cons**

-   Small increase in abstraction

**Decision:** Accepted.

------------------------------------------------------------------------

## Option 3 -- Repository Layer First

``` text
Repository
    ↓
Storage
```

**Decision:** Deferred until repositories are required.

------------------------------------------------------------------------

# Decision

Introduce a `BaseStorage` interface.

Concrete implementations:

-   JSONStorage
-   ParquetStorage (future)
-   IcebergStorage (future)

`BronzeStorage` remains responsible for:

-   Partitioning
-   Folder creation
-   File naming

Serialization is delegated to a storage engine.

------------------------------------------------------------------------

# Resulting Architecture

``` text
               BaseStorage

        save()

        load()

────────────────────────────────

        ▲             ▲

        │             │

JSONStorage    ParquetStorage

        ▲

        │

BronzeStorage
```

------------------------------------------------------------------------

# Consequences

## Positive

-   Separation of concerns
-   Easier migration
-   Better testing
-   Foundation for Trace Core

## Negative

-   One additional abstraction layer

------------------------------------------------------------------------

# SOLID Principles

-   SRP
-   DIP

------------------------------------------------------------------------

# Design Patterns

-   Adapter Pattern
-   Composition over Inheritance

------------------------------------------------------------------------

# Future Work

-   Implement ParquetStorage
-   Refactor BronzeStorage
-   Introduce DuckDB
-   Add Iceberg adapter

------------------------------------------------------------------------

# Decision Summary

Applications depend on **storage capabilities**, not **storage
technologies**.

**Memory Hook**

> Applications ask **what** to store. Storage engines decide **how** to
> store it.
