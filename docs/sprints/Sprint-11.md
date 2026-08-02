# Sprint 11 – Bronze Data Lake Manifest Framework

## Sprint Goal

Introduce a metadata catalog (Manifest) for the Bronze Data Lake to track stored files without scanning the filesystem.

---

## Completed Features

- Implemented Manifest component
- Added manifest loading and persistence
- Automatic metadata registration after each Bronze write
- Hive-style Bronze partition integration
- UTC timestamps for metadata
- File metadata tracking

---

## Architecture

```text
HTTPClient
        │
        ▼
BronzeRecord
        │
        ▼
BronzeStorage
        │
        ├── Write Bronze File
        │
        └── Update Manifest
                │
                ▼
         _manifest.json
```

---

## Metadata Stored

Each Bronze file is registered with:

- Path
- Source
- Market
- Created Timestamp
- File Size

---

## Engineering Concepts Learned

### Data Engineering

- Metadata Catalog
- Data Discovery
- Hive-style Partitioning
- Physical Data Layout

### Software Engineering

- Separation of Concerns
- Single Responsibility Principle
- Component Responsibility

---

## Architectural Decisions

- Metadata separated from business data.
- Manifest owns metadata management.
- BronzeStorage owns persistence.
- UTC timestamps adopted for metadata.

---

## Future Improvements

- Record count
- Schema version
- File format
- Compression metadata
- Checksums
- Data lineage
- Partition statistics

---

## Sprint Outcome

The Bronze layer now behaves like a miniature enterprise Data Lake by maintaining both raw data and a metadata catalog.
