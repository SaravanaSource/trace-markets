# ADR-001: Template Method Pattern

**Status:** Accepted

**Date:** 2026-08-01

## Context
Every ingestion (Demo, API, NSE, BSE, News, RBI, SEBI) follows the same lifecycle:
1. Start ingestion
2. Fetch data
3. Validate
4. Store to Bronze
5. Log completion

Only the fetch logic changes.

## Problem
Avoid duplicating the ingestion workflow while allowing each source to implement its own retrieval logic.

## Decision
Adopt the **Template Method Pattern**.

`BaseIngestion.run()` owns the workflow.
Child classes implement only `fetch()`.

## Trace Markets Architecture

```text
BaseIngestion.run()
        │
        ├── Log start
        ├── fetch()
        ├── BronzeStorage.save()
        ├── Log completion
        └── Return
```

## Benefits
- Eliminates duplication
- Standard lifecycle
- Easier testing
- Easier onboarding
- Centralized logging and storage

## OOP
- Inheritance
- Polymorphism
- Abstraction

## SOLID
- SRP
- OCP

## Production Example
Airflow operators, Spring Batch jobs, ETL frameworks and many ingestion frameworks centralize workflow while subclasses implement only source-specific behavior.

## Consequences
Provides a reusable ingestion framework that all future Trace Markets data sources inherit.
