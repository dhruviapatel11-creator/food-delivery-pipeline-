# Food Delivery Demand Analytics (M2-A1)

## Problem Statement
In rapidly expanding food delivery ecosystems, operational leadership often relies on intuitive heuristics and fragmented spreadsheet logs rather than unified data-driven pipelines. This lack of automated data infrastructure leads to inaccurate peak-demand forecasting, delayed delivery-partner allocations, inconsistent commission calculations, and operational bottlenecks across restaurant zones during rush hours (specifically between 7:00 PM and 9:00 PM). The **Food Delivery Demand Analytics** project establishes an end-to-end Python-based data engineering foundation. It delivers automated data ingestion from REST APIs, robust text and currency cleaning, tiered partner commission calculations via functional programming, object-oriented record management with persistent JSON storage, safe exception handling, and automated unit testing to guarantee operational stability and data integrity.

## Project Features
- **Data Standardization & Hygiene (`src/record_cleaning.py`)**: Strips excess whitespace, standardizes casing, replaces irregular characters, rejects empty/numeric records, and converts raw currency strings into numerical floats with running totals.
- **Functional Commission Engine (`src/fee_calculator.py`)**: Employs pure functions, lambda mappings, tiered rate structures (10%, 15%, 20%), audit filtering, and functional aggregations via `functools.reduce()`.
- **Object-Oriented Record Persistence (`src/record_manager.py`)**: Models domain orders using an `Order` class, providing dictionary serialization (`to_dict`), deserialization (`from_dict`), atomic JSON persistence, and comprehensive `try-except-finally` error handling.
- **Interactive Live Data Pipeline (`src/live_data_pipeline.py`)**: Menu-driven console interface fetching real-time mock restaurant data via REST APIs, creating custom records with validated inputs, running commission analytics, and managing local storage.
- **AI-Augmented Engineering & Debugging (`src/ai_augmented_pipeline.py` & `docs/ai_debugging.md`)**: Demonstrates real-world AI-assisted code generation, boundary-case debugging, resilient HTTP error handling, and structured documentation.
- **Comprehensive Unit Testing Suite (`tests/`)**: Automated test coverage using Python's built-in `unittest` framework validating data cleaning, commission math, edge cases, and serialization integrity.

## Folder Structure
| Directory / File | Description |
| :--- | :--- |
| `food-delivery-pipeline/` | Project root directory |
| ├── `.gitignore` | Configured file patterns to ignore (virtual envs, logs, caches, secrets) |
| ├── `requirements.txt` | External Python project dependencies (`requests`) |
| ├── `git_commands.txt` | Complete command log documenting Git lifecycle, branching, and PR steps |
| ├── `README.md` | Comprehensive project documentation and execution guide |
| ├── `src/` | Primary source code directory |
| │   ├── `record_cleaning.py` | String cleaning, currency extraction, and validation logic |
| │   ├── `fee_calculator.py` | Tiered fee calculator using `map`, `filter`, and `functools.reduce` |
| │   ├── `record_manager.py` | `Order` domain model and JSON disk persistence manager |
| │   ├── `live_data_pipeline.py` | Interactive menu-driven console capstone application |
| │   └── `ai_augmented_pipeline.py` | AI-assisted and human-debugged pipeline script |
| ├── `data/` | Data storage directory |
| │   ├── `raw/` | Ingestion area for raw test files (`orders_sample.txt`, `.gitkeep`) |
| │   └── `processed/` | Destination for cleaned and saved JSON outputs (`records.json`, `.gitkeep`) |
| ├── `docs/` | Conceptual documentation and technical reports |
| │   ├── `section_a_answers.md` | Structured responses for Section A theoretical questions (A1–A6) |
| │   └── `ai_debugging.md` | Prompts, comparative code, and debugging analysis for Section D |
| ├── `tests/` | Unit testing suite |
| │   ├── `test_record_cleaning.py` | Unit tests for string cleaning and currency parsing |
| │   ├── `test_fee_calculator.py` | Unit tests for commission calculation boundaries and aggregations |
| │   └── `test_record_manager.py` | Unit tests for class serialization, deserialization, and file handling |
| └── `screenshots/` | Visual submission artifacts |
|     └── `README.md` | Detailed guidelines on required terminal and Git screenshots |

## Setup Instructions

### Prerequisites
- Python 3.10+ (Verified on Python 3.12.10)
- Git 2.30+ (Verified on Git 2.56.0)

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/food-delivery-pipeline.git
cd food-delivery-pipeline
```

### 2. Environment Setup
Create and activate an isolated Python virtual environment:
```bash
# Windows (PowerShell / Command Prompt)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

> **Note on Mock API**: The live pipeline and AI scripts interface with [JSONPlaceholder](https://jsonplaceholder.typicode.com/posts), an open-access mock REST API simulating restaurant data endpoints (`id` as restaurant ID, `title` as restaurant name).

## Usage Guide

Execute any of the pipeline modules directly from the project root directory:

### Run Record Cleaning Script
```bash
python src/record_cleaning.py
```
*Expected Output*: Displays step-by-step cleaning decisions, flags invalid/empty records, outputs individual order conversions, and prints a final summary with valid count, skipped count, and running total amount.

### Run Fee Calculator Script
```bash
python src/fee_calculator.py
```
*Expected Output*: Displays calculated fees per restaurant based on commission tiers (10%, 15%, 20%), isolated high-value audit records filtered by threshold, and total commission computed via `functools.reduce()`.

### Run Record Manager Script
```bash
python src/record_manager.py
```
*Expected Output*: Instantiates domain orders, serializes and saves records to `data/processed/records.json`, loads records back, safely exercises missing-file exception handling, and concludes with `Operation complete`.

### Run Interactive Live Data Pipeline (Capstone)
```bash
python src/live_data_pipeline.py
```
*Expected Output*: Presents an interactive menu:
1. Fetch and display top 10 mock restaurants via HTTP REST API.
2. Add a new restaurant with validated numeric inputs.
3. Calculate and display commissions using `map()` and `filter()`.
4. Save orders to `data/processed/records.json` and reload them.
5. Exit application.

### Run AI-Augmented Pipeline
```bash
python src/ai_augmented_pipeline.py
```
*Expected Output*: Fetches 5 mock restaurant records, computes tiered commissions on 6 sample order amounts, handles non-200 responses safely, and saves formatted output with `indent=2`.

## Running Automated Unit Tests
Execute the entire test suite from the repository root:
```bash
python -m unittest discover -s tests -v
```
All test cases should pass cleanly without warnings.
