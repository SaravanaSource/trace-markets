# Trace Markets Engineering Design Document

## Epic 1 -- Core Ingestion Framework

**Version:** 0.1\
**Status:** Draft\
**Project:** Trace Markets

------------------------------------------------------------------------

# Purpose

This document explains *why* the current architecture exists, the
alternatives considered, the trade-offs, and how it supports the
long-term vision of Trace Markets.

The goal is to document architectural decisions before implementation so
future engineers (and future me) understand the reasoning instead of
only reading code.

------------------------------------------------------------------------

# Vision

Trace Markets is not a collection of scripts.

It is a **Financial Data Platform** capable of ingesting data from many
providers (NSE, BSE, RBI, SEBI, News APIs, Broker APIs, etc.) and
transforming that data into reliable analytics and AI-powered insights.

Architecture must therefore optimize for:

-   Maintainability
-   Scalability
-   Extensibility
-   Testability
-   Reliability

------------------------------------------------------------------------

# Architecture Overview

``` text
External Source
      │
      ▼
HTTP Client
      │
      ▼
Base Ingestion
      │
      ▼
Validation
      │
      ▼
Bronze Storage
      │
      ▼
Bronze Data Lake
```

------------------------------------------------------------------------

# Problem Statement

Every market data source performs the same lifecycle:

1.  Connect
2.  Fetch
3.  Validate
4.  Store
5.  Log
6.  Return

Only the **fetch logic** changes.

Without a framework this lifecycle becomes duplicated across every
ingestion.

------------------------------------------------------------------------

# Design Goals

-   Single source of truth
-   No duplicated lifecycle code
-   Plug-and-play ingestion sources
-   Replaceable storage implementations
-   Centralized logging
-   Centralized configuration

------------------------------------------------------------------------

# Alternatives Considered

## Option 1 -- Standalone Scripts

Each ingestion performs everything itself.

Pros

-   Very simple
-   Quick prototype

Cons

-   Massive code duplication
-   Hard to test
-   Difficult to scale
-   Difficult to change storage

Decision

❌ Rejected

------------------------------------------------------------------------

## Option 2 -- Shared Framework (Chosen)

A common BaseIngestion owns the workflow while child classes only
implement fetch().

Pros

-   Reusable
-   Consistent
-   Extensible
-   Easier testing
-   Easier maintenance

Cons

-   Slightly more abstraction
-   Initial design effort

Decision

✅ Selected

------------------------------------------------------------------------

# Design Decisions

## BaseIngestion

### Responsibility

Own the ingestion lifecycle.

### Why?

Every ingestion follows the same workflow.

### Child Responsibility

Only implement fetch().

### Pattern

Template Method Pattern

------------------------------------------------------------------------

## BronzeStorage

### Responsibility

Persist raw data.

### Why?

Storage logic should not be duplicated.

### Benefits

-   Future S3 migration
-   Future Azure Blob migration
-   Future Iceberg support

Pattern

Service Layer

------------------------------------------------------------------------

## HTTPClient

### Responsibility

Communicate with external systems.

### Why?

Avoid repeating timeout, logging, retries and authentication.

Future Features

-   Retry policy
-   Authentication
-   Rate limiting
-   Headers
-   Metrics

------------------------------------------------------------------------

## Logging

Centralized using Loguru.

Benefits

-   Consistent formatting
-   Easier debugging
-   Future observability

------------------------------------------------------------------------

## Configuration

Centralized through Settings.

Benefits

-   No hard-coded values
-   Environment support
-   Easier deployment

------------------------------------------------------------------------

# OOP Usage

## Abstraction

BronzeStorage hides filesystem implementation.

HTTPClient hides HTTP implementation.

------------------------------------------------------------------------

## Encapsulation

Each class owns one concern.

------------------------------------------------------------------------

## Composition

BaseIngestion HAS-A BronzeStorage.

APIIngestion HAS-A HTTPClient.

------------------------------------------------------------------------

## Inheritance

APIIngestion inherits BaseIngestion.

------------------------------------------------------------------------

## Polymorphism

Every child overrides fetch().

------------------------------------------------------------------------

# SOLID Principles

## SRP

Each class has one responsibility.

## OCP

Add new storage classes without modifying ingestion classes.

## LSP

Every child ingestion can replace BaseIngestion.

## ISP

Planned through storage/client interfaces.

## DIP

Planned via dependency injection.

------------------------------------------------------------------------

# Layered Architecture

Presentation ↓ Application ↓ Ingestion ↓ Storage ↓ Data Lake

Each layer owns a single concern.

------------------------------------------------------------------------

# Data Lake Strategy

## Bronze

Raw immutable data.

## Silver

Validated and standardized.

## Gold

Business-ready analytics.

------------------------------------------------------------------------

# Why Bronze Exists

Never lose original data.

Allows rebuilding Silver and Gold after bugs or schema changes.

------------------------------------------------------------------------

# Trade-offs

  Decision        Benefit                Cost
  --------------- ---------------------- --------------------------
  BaseIngestion   Less duplication       More abstraction
  BronzeStorage   Storage independence   Extra class
  HTTPClient      Reusable networking    Initial complexity
  Configuration   Flexible deployment    Configuration management
  Logging         Better debugging       Small runtime overhead

------------------------------------------------------------------------

# Future Evolution

Epic 2 - Retry - Exceptions - Metadata

Epic 3 - Dependency Injection - Interfaces

Epic 4 - Metrics - Tracing

Epic 5 - Testing

Epic 6 - NSE - BSE - News

------------------------------------------------------------------------

# Interview Summary

## Why BaseIngestion?

To centralize the ingestion lifecycle and eliminate duplicated workflow
logic.

## Why BronzeStorage?

To separate persistence from business logic and enable future storage
technologies.

## Why HTTPClient?

To centralize HTTP communication and future networking concerns.

## Why Layered Architecture?

To isolate responsibilities, reduce coupling, and improve
maintainability.

------------------------------------------------------------------------

# Key Takeaways

-   Build platforms before features.
-   Separate responsibilities.
-   Centralize shared behaviour.
-   Optimize for future change.
-   Every architectural decision should reduce future maintenance.
