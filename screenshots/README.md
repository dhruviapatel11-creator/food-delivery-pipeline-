# Submission Screenshots Guide

**Project:** Food Delivery Demand Analytics  
**Assessment Code:** M2-A1  

This directory is reserved for screenshots required for your submission. Capture and place the PNG/JPG images here before submitting the project archive or repository URL.

---

## Required Screenshot Checklist

| Screenshot File | Section / Task | What to Display in Terminal / Browser | Required Verification Elements |
| :--- | :--- | :--- | :--- |
| `01_gitignore_status.png` | Section B - Task 1 | `git status` in terminal | Shows `notes.log` is ignored while `data/raw/orders_sample.txt` is untracked. |
| `02_record_cleaning_output.png` | Section B - Task 2 | `python src/record_cleaning.py` | Shows cleaned names, skipped records, running totals, and final summary. |
| `03_fee_calculator_output.png` | Section B - Task 3 | `python src/fee_calculator.py` | Shows `map()` output, `filter()` audit records (> Rs 50), and `reduce()` total fee. |
| `04_record_manager_output.png` | Section B - Task 4 | `python src/record_manager.py` | Shows missing file handling (FileNotFoundError), JSON save/load, and `Operation complete`. |
| `05_record_manager_git_log.png` | Section B - Task 4 | `git log --oneline -n 3` | Shows commit `feat: add record manager with JSON persistence` and previous commits. |
| `06_capstone_api_fetch.png` | Section C - Capstone | `python src/live_data_pipeline.py` (Menu Option 1) | Shows successful REST API fetch of 10 restaurants with HTTP 200 OK. |
| `07_capstone_interactive_add.png` | Section C - Capstone | `python src/live_data_pipeline.py` (Menu Option 2) | Shows validation error re-prompting on non-numeric input and successful order addition. |
| `08_capstone_commission_filter.png`| Section C - Capstone | `python src/live_data_pipeline.py` (Menu Option 3) | Shows commission calculation table and filtered audit items. |
| `09_capstone_json_sync.png` | Section C - Capstone | `python src/live_data_pipeline.py` (Menu Option 4) | Shows saving orders to `records.json` and reloading them into memory. |
| `10_json_file_verification.png` | Section C & D | Open `data/processed/records.json` in VS Code | Shows well-formatted JSON with `indent=2`. |
| `11_ai_pipeline_output.png` | Section D - Task | `python src/ai_augmented_pipeline.py` | Shows 5 mock restaurants fetched, 6 tiered commissions, and file save. |
| `12_unittest_results.png` | Test Suite | `python -m unittest discover -s tests -v` | Shows all 17 unit tests passing with `OK`. |
| `13_git_feature_branch_pr.png` | Git Workflow | GitHub Pull Request Webpage | Shows PR from feature branch into `main` with reviewed status. |
| `14_git_merged_history.png` | Git Workflow | `git log --graph --oneline` | Shows at least 5 commits on `main` and merged feature branch. |

---

## Step-by-Step Instructions to Capture Each Screenshot

### Screenshot 1: Git Status (.gitignore Verification)
1. Open PowerShell or Git Bash in `food-delivery-pipeline`.
2. Run:
   ```bash
   git status
   ```
3. Capture your terminal window showing:
   - `Untracked files: data/raw/orders_sample.txt`
   - `notes.log` does **NOT** appear anywhere in the output.
4. Save as `screenshots/01_gitignore_status.png`.

### Screenshot 2: Record Cleaning Script
1. Run:
   ```bash
   python src/record_cleaning.py
   ```
2. Capture the output showing valid records, skipped records, and execution summary.
3. Save as `screenshots/02_record_cleaning_output.png`.

### Screenshot 3: Fee Calculator Script
1. Run:
   ```bash
   python src/fee_calculator.py
   ```
2. Capture the output showing mapped records, audit-flagged records (> Rs 50), and total fee (Rs 474.60).
3. Save as `screenshots/03_fee_calculator_output.png`.

### Screenshot 4: Record Manager Script
1. Run:
   ```bash
   python src/record_manager.py
   ```
2. Capture the output displaying TEST 1, TEST 2, TEST 3, and `Operation complete`.
3. Save as `screenshots/04_record_manager_output.png`.

### Screenshot 5: Git Log for Record Manager (At Least 2 Commits)
1. Run:
   ```bash
   git log --oneline -n 4
   ```
2. Capture the terminal displaying `feat: add record manager with JSON persistence`.
3. Save as `screenshots/05_record_manager_git_log.png`.

### Screenshot 6–9: Live Data Pipeline (Capstone)
1. Run:
   ```bash
   python src/live_data_pipeline.py
   ```
2. Execute Option 1 (Fetch mock restaurants) -> Capture as `06_capstone_api_fetch.png`.
3. Execute Option 2 (Add order, enter an invalid string like `"abc"` for amount to demonstrate validation re-prompting) -> Capture as `07_capstone_interactive_add.png`.
4. Execute Option 3 (Calculate commission) -> Capture as `08_capstone_commission_filter.png`.
5. Execute Option 4 (Save to JSON & reload) -> Capture as `09_capstone_json_sync.png`.

### Screenshot 10: JSON File Verification
1. Open `data/processed/records.json` in your editor.
2. Capture the window displaying the structured JSON payload indented with 2 spaces.
3. Save as `screenshots/10_json_file_verification.png`.

### Screenshot 11: AI-Augmented Pipeline
1. Run:
   ```bash
   python src/ai_augmented_pipeline.py
   ```
2. Capture the terminal output.
3. Save as `screenshots/11_ai_pipeline_output.png`.

### Screenshot 12: Unit Test Results
1. Run:
   ```bash
   python -m unittest discover -s tests -v
   ```
2. Capture the 17 passed tests and final `OK`.
3. Save as `screenshots/12_unittest_results.png`.

### Screenshot 13 & 14: GitHub Pull Request & Merged Git Log
1. Once pushed to GitHub, capture the merged Pull Request interface in your browser (`13_git_feature_branch_pr.png`).
2. Run `git log --graph --oneline` in your terminal and capture the branch merge graph (`14_git_merged_history.png`).
