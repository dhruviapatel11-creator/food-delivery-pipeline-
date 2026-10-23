# Section A: Concept Application — Written Answers

**Assessment Code:** M2-A1  
**Module:** Module 1 (Introduction to Data Science & Git/GitHub) & Module 2 (Python for Data Science)  
**Project:** Food Delivery Demand Analytics  

---

## A1. Data Science Lifecycle & Generative AI Integration in Demand Forecasting

### Problem Context & Lifecycle Walkthrough
To transition the food delivery startup from subjective "gut feeling" decision-making to an automated, predictive operational paradigm for forecasting peak demand between 7:00 PM and 9:00 PM across restaurant zones, the team must execute all six stages of the Data Science Lifecycle:

1. **Problem Definition:**  
   The team frames the operational challenge into a quantifiable machine learning problem. The business objective is to forecast hourly order volumes for predefined geographic restaurant clusters during the 7:00 PM–9:00 PM dinner window to optimize driver dispatching and delivery-partner incentives.  
   *Concrete Deliverable:* A formal **Project Charter and Requirements Specification Document** detailing key performance indicators (e.g., target Mean Absolute Error $\le 8$ orders/zone, latency constraints $\le 200\text{ ms}$), defined spatial boundaries (zones/hexagons), and evaluation metrics.

2. **Data Collection:**  
   Historical data spanning two years stored in fragmented spreadsheets (.xlsx, .csv) is aggregated alongside external operational signals, including merchant preparation timestamps, delivery partner logs, rain/temperature weather data, and local public events.  
   *Concrete Deliverable:* A consolidated, raw **Tabular Dataset / Staging Database Schema** with consistent primary/foreign keys (e.g., `zone_id`, `order_timestamp`, `restaurant_id`, `order_value`, `weather_condition`).

3. **Data Preparation (Data Cleaning & Feature Engineering):**  
   Raw historical logs contain missing values, duplicate entries, cancelled orders, irregular timezone offsets, and string formatting errors. The team cleans numerical fields, strips formatting noise, imputes missing values, and engineers predictive features such as rolling average orders over the past 30 minutes, lag features (same day last week), day-of-week indicators, and precipitation flags.  
   *Concrete Deliverable:* A validated, versioned **Cleaned Feature Store / Preprocessed Modeling Matrix** split into training, validation, and holdout test sets without data leakage.

4. **Exploration (Exploratory Data Analysis - EDA):**  
   Analysts conduct statistical distributions, zone-level demand heatmaps, correlation analyses, and temporal time-series decompositions to detect demand seasonality, demand spikes during weekend rush hours, and outlier delivery zones.  
   *Concrete Deliverable:* An interactive **EDA Report with Visual Diagnostic Dashboards** summarizing peak order distributions, zone-level demand variance, and feature importance correlations.

5. **Modelling:**  
   The team trains and tunes predictive regression and time-series algorithms (e.g., LightGBM, XGBoost, Random Forests, or SARIMAX) to predict the numerical volume of orders for each zone between 7:00 PM and 9:00 PM given current and historical signals.  
   *Concrete Deliverable:* A serialized, trained **Model Artifact (`.pkl` / `.joblib`)** with hyperparameter tuning logs and reproducible training pipelines.

6. **Evaluation:**  
   The model is rigorously scored against the unseen test dataset using metrics such as Root Mean Squared Error (RMSE), Mean Absolute Percentage Error (MAPE), and operational backtesting against historical dispatch failures.  
   *Concrete Deliverable:* A comprehensive **Model Evaluation & Business Impact Report** demonstrating how model-driven driver positioning reduces delivery delays by target percentages compared to historical baseline heuristics.

### Generative AI Acceleration & Risk Analysis
- **Stage 1 for Generative AI — Data Preparation (Feature Engineering & Pipeline Code Synthesis):**  
  *Task Assisted:* Generative AI tools (e.g., GitHub Copilot or LLM code assistants) can dramatically accelerate writing complex data transformation pipelines, generating vectorized Pandas/NumPy routines for window functions (e.g., 7-day exponentially weighted rolling averages), and parsing irregular timestamp/string formats.  
  *Unreviewed AI Risk:* AI code generators can introduce subtle **Data Leakage** bugs—such as computing global rolling statistics or target encodings across both training and test partitions simultaneously—or quietly handle `NaN` values using forward-fills that look valid syntactically but mathematically invalidate model reliability.

- **Stage 2 for Generative AI — Exploration (Automated Analysis & Visual Reporting):**  
  *Task Assisted:* Generative AI can assist analysts by drafting boilerplate exploratory visualization scripts (Matplotlib/Seaborn plots for zone heatmaps and demand curves) and synthesizing executive summaries from descriptive statistical summaries.  
  *Unreviewed AI Risk:* LLMs are prone to **Plausible Hallucination and Spurious Correlation Synthesis**. Without human analytical review, an AI tool might generate a compelling narrative asserting that a specific zone's demand correlates strongly with an irrelevant external variable or misinterpret cyclical seasonality as permanent growth, leading leadership to deploy fleet resources to incorrect geographic zones.

---

## A2. Git Branching Strategy, Collaborative Workflow, and Merge Conflict Resolution

### Branching Strategy Rationale
When three developers collaborate on shared codebases (data cleaning, reporting, order tracking), pushing directly to the `main` branch creates constant integration collisions, overwrites incomplete functions, and breaks production stability.  
A **Feature Branch Workflow** (Git Flow derivative) resolves this coordination bottleneck:
1. The `main` branch is designated as protected and production-ready; direct pushes to `main` are disallowed.
2. Each developer branches off `main` into dedicated, isolated branches (e.g., `feature/data-cleaning`, `feature/reporting`, `feature/order-tracking`).
3. Developers work independently without breaking teammates' environments.
4. Changes are integrated back into `main` strictly through **Pull Requests (PRs)** accompanied by peer code review and automated checks.

### Exact Sequence of Git Commands
Here is the step-by-step command sequence each developer follows:

```bash
# 1. Ensure local main is synchronized with the remote upstream
git checkout main
git pull origin main

# 2. Create and switch to an isolated feature branch
git checkout -b feature/order-tracking

# 3. Work on code, stage atomic modifications, and commit with conventional messages
git add src/order_tracking.py
git commit -m "feat: implement order tracking state machine and status updates"

# 4. Synchronize latest updates from main before publishing
git fetch origin
git merge origin/main

# 5. Push the feature branch to the remote repository
git push -u origin feature/order-tracking

# 6. Raise a Pull Request on GitHub/GitLab:
#    - Submit PR comparing feature/order-tracking -> main
#    - Request code review from teammates (cleaning and reporting devs)
#    - Pass automated tests and address review comments

# 7. Complete the reviewed merge (via PR UI or terminal once approved)
git checkout main
git pull origin main
git branch -d feature/order-tracking
```

### Realistic Merge Conflict Scenario & Resolution
- **Realistic Scenario:**  
  Suppose both Developer A (`feature/data-cleaning`) and Developer C (`feature/order-tracking`) modify the shared configuration dictionary or record schema in `src/record_manager.py` on the exact same lines (e.g., adding a new field to `DEFAULT_SCHEMA = {"id": int, "name": str}`). Developer A merges their PR into `main` first. When Developer C attempts to merge `main` into their feature branch, Git halts and flags a conflict in `src/record_manager.py`:
  ```python
  <<<<<<< HEAD (feature/order-tracking)
  DEFAULT_SCHEMA = {"id": int, "name": str, "delivery_time_minutes": int, "is_delivered": bool}
  =======
  DEFAULT_SCHEMA = {"id": int, "name": str, "cleaned_name": str, "source_format": str}
  >>>>>>> main
  ```

- **Step-by-Step Resolution:**
  1. Developer C runs `git status` to identify unmerged paths (`src/record_manager.py`).
  2. Developer C opens the file in their editor, reviews the conflicting markers, and talks with Developer A to understand both requirements.
  3. Developer C combines both requirements into a unified schema, removing all conflict divider markers (`<<<<<<<`, `=======`, `>>>>>>>`):
     ```python
     DEFAULT_SCHEMA = {
         "id": int,
         "name": str,
         "cleaned_name": str,
         "source_format": str,
         "delivery_time_minutes": int,
         "is_delivered": bool
     }
     ```
  4. Developer C runs unit tests to verify the merged code behaves properly without regressions.
  5. Developer C stages the resolved file and commits the merge:
     ```bash
     git add src/record_manager.py
     git commit -m "fix: resolve schema merge conflict between order tracking and cleaning"
     git push origin feature/order-tracking
     ```
  6. The PR updates cleanly, enabling the final reviewed merge into `main`.

---

## A3. Functional Programming for Commission Automation: `map()`, `filter()`, and `functools.reduce()`

### Architecture: Named Function with `map()` and `lambda`
To replace error-prone manual spreadsheets with an automated, predictable payout system, commission calculation logic must be encapsulated in a pure, testable named function. A named function isolates business rules (tier thresholds, percentages, tax adjustments) from iteration mechanics.

```python
import functools

# Pure named calculation function
def calculate_tiered_commission(amount: float) -> float:
    """Calculates tiered commission: 10% (<=200), 15% (201-500), 20% (>500)."""
    if amount <= 200.0:
        return round(amount * 0.10, 2)
    elif amount <= 500.0:
        return round(amount * 0.15, 2)
    else:
        return round(amount * 0.20, 2)
```

Applying this via `map()` with a `lambda` over an order list:
```python
orders = [
    {"id": 101, "restaurant": "Tandoori Nights", "amount": 150.0},
    {"id": 102, "restaurant": "Spice Bazaar", "amount": 320.0},
    {"id": 103, "restaurant": "Royal Punjab", "amount": 650.0},
]

# Using map with a lambda to enrich each record with its computed fee
records_with_fees = list(map(
    lambda order: {**order, "fee": calculate_tiered_commission(order["amount"])},
    orders
))
```

### Why `map()` is More Appropriate than a Second `for` Loop
1. **Immutability and Pure Transformations:** Writing an imperative `for` loop encourages state mutation (e.g., modifying dictionaries in-place or appending to external lists via `.append()`). In contrast, `map()` promotes declarative functional transformations where raw input records remain immutable, preventing side effects across downstream data pipelines.
2. **Lazy Evaluation & Memory Efficiency:** In Python, `map()` returns an iterator that computes items on-demand rather than allocating an entire duplicate list in memory at once. For large-scale delivery workloads processing hundreds of thousands of daily records, iterator pipelines significantly decrease peak RAM utilization.
3. **Separation of Concerns:** A `for` loop commingles the mechanics of iteration (indices, loop counters, temporary variables) with the business logic. `map()` cleanly abstracts the traversal, making the code expressive, concise, and trivial to unit-test.

### Role of `filter()` in Financial Audits
The finance team frequently requires subsets of records for regulatory or high-payout audits (e.g., all deliveries generating commissions strictly greater than Rs 50.00).  
`filter()` applies a boolean predicate across the sequence without imperative branching inside calculation loops:
```python
AUDIT_THRESHOLD = 50.00
audit_records = list(filter(lambda record: record["fee"] > AUDIT_THRESHOLD, records_with_fees))
```
`filter()` extracts only compliant records, producing a self-documenting audit partition without mutating the original sequence.

### Aggregation with `functools.reduce()` in a Single Expression
While `sum()` works for simple lists of numbers, `functools.reduce()` provides generalized functional folding across collections of complex dictionary objects:
```python
total_commission = functools.reduce(
    lambda accumulator, record: accumulator + record["fee"],
    records_with_fees,
    0.0
)
```
In a single immutable expression, `functools.reduce()` aggregates the total commission across the entire dataset by accumulating the `'fee'` key from each dictionary starting from the initial accumulator seed (`0.0`), eliminating accumulator initialization bugs outside loops.

---

## A4. Object-Oriented Modeling: Inheritance, Method Overriding, and Defensive Base Class Design

### Modeling Multi-User Profiles with Inheritance
An object-oriented design establishes a parent `User` base class containing common domain attributes (`user_id`, `name`, `email`, `role`) while specialized subclasses (`Customer`, `DeliveryPartner`, `Admin`) extend this foundation and override `display_profile()` to present tailored summaries:

```python
class User:
    def __init__(self, user_id: int, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email

class Customer(User):
    def __init__(self, user_id: int, name: str, email: str, delivery_address: str):
        super().__init__(user_id, name, email)
        self.delivery_address = delivery_address

    def display_profile(self) -> str:
        return f"[Customer] #{self.user_id} {self.name} | Address: {self.delivery_address}"

class DeliveryPartner(User):
    def __init__(self, user_id: int, name: str, email: str, vehicle_number: str, rating: float):
        super().__init__(user_id, name, email)
        self.vehicle_number = vehicle_number
        self.rating = rating

    def display_profile(self) -> str:
        return f"[DeliveryPartner] #{self.user_id} {self.name} | Vehicle: {self.vehicle_number} | Rating: {self.rating}★"

class Admin(User):
    def __init__(self, user_id: int, name: str, email: str, access_level: str):
        super().__init__(user_id, name, email)
        self.access_level = access_level

    def display_profile(self) -> str:
        return f"[Admin] #{self.user_id} {self.name} | Clearance: {self.access_level}"
```

### The Runtime Problem: `AttributeError` in Polymorphic Traversal
If a developer creates a heterogeneous list containing various user instances and iterates over them:
```python
user_roster = [Customer(1, "Aarav", "a@test.com", "Zone 4"), Admin(2, "Priya", "p@test.com", "SuperAdmin"), ...]
for user in user_roster:
    print(user.display_profile())
```
If `display_profile()` is implemented only on *some* subclasses and omitted from the base class or a newly introduced subclass (e.g., a junior developer adds `CorporateClient(User)` without defining `display_profile()`), Python raises an unhandled:
```text
AttributeError: 'CorporateClient' object has no attribute 'display_profile'
```
This halts execution at runtime mid-loop, crashing the application and failing to process any remaining users.

### Defensive Redesign of the Base Class
To guarantee that the loop never crashes regardless of which new subclass is introduced in the future, we employ Python's `abc` (Abstract Base Class) module alongside an enforceable abstract interface or a safe fallback implementation:

#### Approach 1: Enforceable Interface with `abc.ABC` and `@abstractmethod`
```python
from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, user_id: int, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email

    @abstractmethod
    def display_profile(self) -> str:
        """Abstract contract: all derived subclasses MUST implement this method."""
        pass
```
*Why this prevents runtime crashes:* Python will refuse to instantiate any subclass that fails to implement `display_profile()`, raising a `TypeError` at instantiation time during development/testing rather than an unexpected `AttributeError` during a production batch loop.

#### Approach 2: Safe Default Base Implementation (Polymorphic Fallback)
```python
class User:
    def __init__(self, user_id: int, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email

    def display_profile(self) -> str:
        """Default fallback representation ensuring all subclasses respond safely."""
        return f"[{self.__class__.__name__}] #{self.user_id} {self.name} ({self.email})"
```
With this architecture, if any future subclass omits an explicit override, Python's Method Resolution Order (MRO) cleanly resolves to the parent `User.display_profile()` method. The polymorphic loop executes smoothly without exceptions.

---

## A5. HTTP Status Code Handling and Atomic Persistence via `try-except-finally`

### Detailed Analysis of HTTP Status Codes
When integrating a third-party payment gateway or external data API into the backend, each HTTP response status code conveys a distinct protocol state requiring specific handling:

1. **`200 OK`:**  
   *Meaning:* The API request succeeded, and the server returned the requested payment or transaction resource.  
   *Action:* Validate that the response body is non-empty, safely parse the JSON payload via `response.json()`, extract required confirmation IDs, and proceed with order state transition.

2. **`401 Unauthorized`:**  
   *Meaning:* Authentication credentials (e.g., API Bearer token, merchant key, or signature) are missing, expired, or invalid.  
   *Action:* The script must **not** blindly retry with the same credentials. It should log a high-severity security alert, trigger an automatic token refresh routine (if OAuth2 is supported), notify system administrators, and halt the transaction securely.

3. **`429 Too Many Requests` (Rate Limited):**  
   *Meaning:* The food delivery backend has exceeded the payment gateway's rate limits (e.g., max 100 requests per minute).  
   *Action:* Inspect the `Retry-After` HTTP header. The script should pause execution using exponential backoff with jitter (`time.sleep()`), and then retry the request up to a maximum retry limit rather than aborting.

4. **`500 Internal Server Error`:**  
   *Meaning:* An unhandled crash or database failure occurred within the third-party payment gateway's servers.  
   *Action:* The script must treat this as a temporary upstream failure. It should log the request incident ID, avoid crashing, queue the transaction for an asynchronous background retry, and return a graceful failure notice to the user.

### Why the Script Crashed and Corrupted the File Mid-Write
The teammate's script likely opened the target file in write mode (`open('records.json', 'w')`), immediately truncating existing contents to zero bytes. When the API returned a 500 error while the file handle was open or mid-stream, an unhandled exception crashed the script. Because the file was neither flushed nor closed properly—or was left partially written—the entire storage file was left corrupted or empty.

### How `try-except-finally` Guarantees Data Integrity
Wrapping the file input/output in a `try-except-finally` block prevents corruption:

```python
import json
import os
import tempfile

def safe_save_records(records_data: list, target_filepath: str) -> bool:
    temp_file = None
    try:
        # Step 1: Write to a temporary file first (Atomic Write Pattern)
        dir_name = os.path.dirname(target_filepath) or "."
        with tempfile.NamedTemporaryFile("w", dir=dir_name, delete=False, encoding="utf-8") as temp_file:
            json.dump(records_data, temp_file, indent=2)
            temp_file.flush()
            os.fsync(temp_file.fileno())  # Ensure bytes reach physical disk
        
        # Step 2: Atomically replace the destination file
        os.replace(temp_file.name, target_filepath)
        return True

    except Exception as e:
        print(f"[ERROR] Transaction failed: {e}. Output file preserved intact.")
        # Clean up temporary file if write was interrupted
        if temp_file and os.path.exists(temp_file.name):
            try:
                os.remove(temp_file.name)
            except OSError:
                pass
        return False

    finally:
        # What finally guarantees:
        # This block executes unconditionally — regardless of whether the try block
        # succeeded, caught an exception, or encountered a return statement.
        print("Operation complete: Database file locks released and resources verified.")
```

#### What `finally` Guarantees and Why It Always Executes
The `finally` clause guarantees execution under all circumstances:
- If the `try` block succeeds without error, `finally` runs immediately before exiting.
- If an exception occurs (e.g., `requests.exceptions.HTTPError` on a 500 status code), execution jumps to `except`, runs the handler, and then executes `finally`.
- Even if an unhandled exception occurs or a return statement is triggered within `try` or `except`, the Python runtime pauses return propagation, executes the `finally` block to completion, and then resumes normal execution flow. This guarantees critical resources (file handles, network sockets, database locks) are released cleanly.

---

## A6. Regular Expressions for Contact Records Hygiene: `re` Module, Pattern Design, and Edge Cases

### Pattern Architecture in Words
To validate and extract valid Indian customer contact numbers from noisy textual records, we construct a comprehensive regular expression pattern. Described in words:
1. **Optional Country Code:** The pattern begins with an optional country code prefix consisting of an optional plus symbol (`+`) followed by `91` (or leading `0`), optionally followed by a delimiter (space or hyphen).
2. **First Digit (Mobile Carrier Allocation):** In the Indian telecommunications numbering plan, valid mobile numbers must begin with digits `6`, `7`, `8`, or `9`.
3. **Subsequent Digits:** Followed by exactly 9 numerical digits (making a 10-digit mobile number), allowing optional grouping delimiters (hyphens or spaces) after the 5th digit (e.g., `XXXXX XXXXX` or `XXXXX-XXXXX`).
4. **Boundary Anchoring:** Enclosed within word boundaries (`\b`) to prevent matching partial numbers embedded in longer alphanumeric strings (e.g., order IDs or tracking hashes).

In Python syntax, this pattern is represented as:
```python
import re

PHONE_REGEX = re.compile(r'\b(?:\+91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}\b')
```

### Why `re.findall()` is More Appropriate than `re.search()`
- **`re.search()` Limitations:** `re.search()` scans through the string and stops at the very first match it finds, returning a single `Match` object (or `None`). In a customer contact records file containing thousands of records or multiple contacts per paragraph, `re.search()` extracts only the first customer's number and ignores all subsequent entries, requiring manual pointer management or loop slicing.
- **`re.findall()` Advantages:** `re.findall()` scans the entire text buffer from start to finish in a single optimized C-level pass. It identifies every non-overlapping substring that conforms to the regular expression pattern and returns them directly as a clean Python list of strings. This is directly aligned with batch ETL data preparation.

### Real-World Formatting Edge Cases
A naive pattern—such as `r'\d{10}'` (any sequence of 10 consecutive digits)—fails significantly in production:

1. **Incorrect Acceptance (False Positive):**  
   A naive pattern accepts strings like `"0000000000"`, `"1234567890"`, or alphanumeric order tracking codes like `"ORD19876543210"` (extracting `"1987654321"`). None of these correspond to genuine telecommunication subscribers. Moreover, it accepts customer pin codes concatenated with order amounts (e.g., `560001` + `2500` = `5600012500`).
2. **Incorrect Rejection (False Negative):**  
   A naive pattern rejects valid customer inputs entered with formatting standards like `"+91 98765-43210"` or `"(+91) 9876543210"` because the presence of the `+`, parentheses, spaces, or hyphens breaks the consecutive digit sequence.  
   A robust regex pattern accommodates standardized optional formatting while strictly enforcing carrier starting digits (`[6-9]`) and total digit counts.
