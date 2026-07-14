# ATR – Automated Test Reconciliation Engine

## Overview

**ATR (Automated Test Reconciliation) Engine** is a metadata-driven Python framework designed to compare datasets from multiple data sources and generate comprehensive reconciliation reports. The engine validates data consistency by classifying every record into exactly one of four categories: **Matched**, **Mismatched**, **Source Only**, or **Target Only** — based on configurable comparison rules.

The primary objective is to automate data validation during ETL testing, data migration, database modernization, and system integration testing — reducing manual effort while improving accuracy and reliability.

---

## Features

- Compare datasets from multiple sources:
  - CSV
  - Excel (`.xlsx`)
  - TSV
  - Database *(Planned — Oracle, Snowflake, PostgreSQL)*
- Metadata-driven execution via `driverconfig.xlsx`
- Batch execution: run multiple test cases in a single invocation
- Support for single and composite comparison keys
- Row-by-row comparison when no comparison key is configured
- Comprehensive pre-reconciliation validation:
  - Driver configuration validation
  - Source and target file/database existence and accessibility
  - Schema validation (column names and counts)
  - Duplicate key detection
- Configurable comparison options:
  - `ignore_whitespace` — trim leading/trailing spaces
  - `ignore_case` — case-insensitive string comparison
- Column-order-independent comparison (columns matched by name)
- Detailed per-column mismatch identification
- Per-test-case output folder with full result artefacts
- Interactive HTML reconciliation report *(Planned)*
- Graceful error handling: failed test cases do not block remaining ones

---

## Project Goals

- Automate data reconciliation across heterogeneous data sources.
- Minimise manual comparison effort.
- Provide accurate, actionable reconciliation reports.
- Support reusable and configurable validation workflows.
- Build a scalable, extensible framework for future data source support.

---

## Supported Input Sources

| Source Type      | Status              |
|------------------|---------------------|
| CSV              | ✅ Supported (MVP)  |
| Excel (`.xlsx`)  | ✅ Supported (MVP)  |
| TSV              | 🚧 Planned          |
| Database (Oracle, Snowflake, PostgreSQL) | 🚧 Planned |
| Parquet          | 🚧 Planned          |
| JSON             | 🚧 Planned          |

---

## Reconciliation Categories

Every record is classified into **exactly one** of the following categories:

| Category        | Description                                              |
|-----------------|----------------------------------------------------------|
| ✅ Matched       | Record exists in both datasets and all columns match     |
| ❌ Mismatched    | Record exists in both datasets but one or more columns differ |
| ➕ Source Only   | Record exists in the source dataset but not in target    |
| ➕ Target Only   | Record exists in the target dataset but not in source    |

---

## Validation Rules

Before reconciliation begins, the engine performs the following validations:

### Driver Configuration Validation
- All mandatory fields must be populated.
- Invalid or missing configuration fails the current test case.

### Source & Target Validation
- Source/target file exists and is accessible.
- File format is supported and can be opened.
- *(Database)* Connection is successful, credentials are valid, table exists, query executes successfully.

### Dataset Validation
- Dataset loaded successfully and contains headers.
- Dataset is not corrupted.
- Empty datasets are reported (not treated as errors); metadata is displayed.

If any validation fails, reconciliation for that test case is stopped and an appropriate error is recorded. Remaining test cases continue.

---

## Comparison Rules

| Rule | Description |
|------|-------------|
| **Record Matching** | If `compare_key` is set, records are matched by key; otherwise row-by-row by original order |
| **Key Comparison** | Key in both → column comparison; key in source only → Source Only; key in target only → Target Only |
| **Column Comparison** | Every comparable column is compared; all match → Matched; any differ → Mismatched |
| **Ignore Case** | When `Y`, character-case differences are ignored |
| **Ignore Whitespace** | When `Y`, leading/trailing whitespace is stripped before comparison |
| **Column Order** | Column order does not matter; columns are mapped by name |
| **Mismatch Detail** | Every differing column is identified with compare key, column name, source value, and target value |

---

## Configuration

Execution is driven by `resource/driverconfig.xlsx`. The engine reads this file and runs every row where `run_flag = Y`.

### Driver Configuration Fields

| Field               | Description                                                  |
|---------------------|--------------------------------------------------------------|
| `run_flag`          | `Y` to execute, `N` to skip                                  |
| `testcase_name`     | Name of the test case                                        |
| `source_name`       | Friendly name for the source dataset                         |
| `source_type`       | Source type (`CSV`, `Excel`, `Database`, …)                 |
| `source_file`       | Source filename (relative to `resource/source/`)             |
| `target_name`       | Friendly name for the target dataset                         |
| `target_type`       | Target type (`CSV`, `Excel`, `Database`, …)                 |
| `target_file`       | Target filename (relative to `resource/target/`)             |
| `compare_key`       | Column(s) used as the comparison key (comma-separated for composite keys) |
| `ignore_whitespace` | `Y` / `N`                                                   |
| `ignore_case`       | `Y` / `N`                                                   |

### Sample Configuration Row

| run_flag | testcase_name        | source_type | source_file       | target_type | target_file       | compare_key | ignore_whitespace | ignore_case |
|----------|----------------------|-------------|-------------------|-------------|-------------------|-------------|-------------------|-------------|
| Y        | Customer Validation  | Excel       | source_data.xlsx  | Excel       | target_data.xlsx  | Customer_ID | Y                 | Y           |

---

## High-Level Workflow

```text
Read Driver Configuration (driverconfig.xlsx)
        │
        ▼
For each test case where run_flag = Y:
        │
        ├── Validate Driver Configuration
        │
        ├── Validate Source & Target (file / database)
        │
        ├── Load Source & Target Datasets
        │
        ├── Validate Schema (column names, column count)
        │
        ├── Validate Compare Keys (existence, duplicates)
        │
        ├── Normalize Data (ignore_case / ignore_whitespace)
        │
        ├── Compare Records (key-based or row-by-row)
        │
        ├── Categorize Results
        │       ├── Matched
        │       ├── Mismatched (with column-level diff)
        │       ├── Source Only
        │       └── Target Only
        │
        ├── Generate Output Files
        │
        └── Mark Test Case PASSED / FAILED
        │
        ▼
Generate Batch Summary Report
```

---

## Output Files

For every executed test case, a dedicated output folder is created containing:

| File                      | Description                                    |
|---------------------------|------------------------------------------------|
| `Summary.xlsx`            | Reconciliation summary in Excel format         |
| `Matched.csv`             | All matched records                            |
| `Mismatched.csv`          | Mismatched records with column-level diff      |
| `SourceOnly.csv`          | Records present only in source                 |
| `TargetOnly.csv`          | Records present only in target                 |
| `Report.html`             | Interactive HTML reconciliation report *(Planned)* |
| `Summary_report.txt`      | Plain-text execution summary                   |
| `driverconfig.xlsx`       | Snapshot of the current test case configuration |
| `utilityconfig.ini`       | Database config snapshot *(Database mode)*     |
| `source_original_data.csv`| Original source dataset                        |
| `target_original_data.csv`| Original target dataset                        |

---

## Batch Execution

- All test cases with `run_flag = Y` are executed sequentially in a single run.
- Each test case is independently validated and executed.
- A failure in one test case does **not** stop the remaining test cases.
- At the end, an overall **Batch Summary** is generated:

| Metric               | Description                     |
|----------------------|---------------------------------|
| Total Test Cases     | Total rows in driverconfig       |
| Passed               | Test cases that completed successfully |
| Failed               | Test cases that encountered an error   |
| Skipped              | Test cases with `run_flag = N`  |
| Overall Status       | PASS / FAIL                     |

---

## Error Handling

| Error Category         | Strategy                                                       |
|------------------------|----------------------------------------------------------------|
| Configuration Errors   | Mark test case FAILED, log error, continue                     |
| Input / File Errors    | Mark test case FAILED, log error, continue                     |
| Validation Errors      | Mark test case FAILED, log error, continue                     |
| Comparison Errors      | Mark test case FAILED, log error, continue                     |
| Report Generation Errors | Log error, continue                                         |
| System / Engine Errors | Stop entire engine only on unrecoverable failures (OOM, crash) |

---

## Project Structure

```text
ATR-recon/
│
├── README.md
├── pyproject.toml               # Project metadata and dependencies
├── .python-version              # Python 3.14
├── .gitignore
│
├── Docs/
│   ├── 00_Project_Structure.md
│   └── 02_Functional_Specification.md
│
├── resource/
│   ├── driverconfig.xlsx        # Master execution and mapping config
│   ├── source/
│   │   └── source_data.xlsx     # Source dataset
│   └── target/
│       └── target_data.xlsx     # Target dataset
│
├── src/
│   ├── config.py                # Path configuration
│   ├── data_compy.py            # Data comparison module (datacompy)
│   └── main.py                  # Engine entry point
│
└── .venv/                       # Virtual environment (uv-managed)
```

> **Planned additions:** `logs/`, `output/`, `tests/`, `config/utilityconfig.ini`

---

## Tech Stack

| Component      | Library / Tool        | Version Requirement |
|----------------|-----------------------|---------------------|
| Language       | Python                | ≥ 3.14              |
| Data Processing | Pandas               | ≥ 3.0.3             |
| Data Comparison | datacompy            | ≥ 1.0.2             |
| Excel I/O      | OpenPyXL              | (via pandas)        |
| Package Manager | uv                   | —                   |
| Testing        | Pytest                | *(Planned)*         |

---

## Installation

### Prerequisites
- Python 3.14+
- [`uv`](https://github.com/astral-sh/uv) package manager

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd ATR-recon

# Create virtual environment and install dependencies
uv sync

# Activate virtual environment
# Windows:
.venv\Scripts\activate
```

---

## Usage

1. Place your source dataset in `resource/source/`
2. Place your target dataset in `resource/target/`
3. Configure test cases in `resource/driverconfig.xlsx`
4. Run the engine:

```bash
python src/main.py
```

Results will be generated in the `output/` folder, one sub-folder per test case.

---

## Use Cases

- ETL Testing
- Data Migration Validation
- Database Modernization Testing
- Data Warehouse Testing
- System Integration Testing
- Regression Testing
- Data Quality Validation

---

## Future Enhancements

- Database connectivity (Oracle, Snowflake, PostgreSQL, MySQL)
- Interactive HTML reconciliation reports with charts
- Formatted Excel reconciliation reports
- Great Expectations integration for pre-reconciliation data quality checks
- Performance optimisation for large datasets (chunk-based and parallel processing)
- Command-line interface (CLI)
- Structured logging framework
- YAML/JSON configuration support (alternative to Excel driver config)
- Column-level comparison rules and exclusion lists
- Data type-specific normalisation
- Execution analytics dashboard

---

## Project Status

**Current Phase:** 🚧 Minimum Viable Product (MVP)

The MVP focuses on a configurable reconciliation engine for CSV and Excel datasets with robust validation and reporting. Database connectivity, HTML reports, and advanced comparison capabilities are planned for future releases.

---

## License

This project is developed for learning, experimentation, and portfolio purposes. Feel free to fork, extend, and customise it.

---

## Author

**Sureshkumar V**

**Skills:** Python • SQL • Pandas • ETL Testing • Data Validation • Automation • Data Engineering
