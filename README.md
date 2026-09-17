# Property Risk Tracker

![Tests](https://github.com/mariocab114/Property-Risk-Tracker/actions/workflows/tests.yml/badge.svg)

A Python command-line application for tracking commercial property risk. Property data lives in a normalized **MS SQL Server** database, exposure rankings are calculated by a **T-SQL stored procedure**, and a **scikit-learn K-Means** model segments properties into risk tiers.

## Features

- **Manage properties:** add, view, update, and delete property records
- **Exposure ranking:** a parameterized T-SQL stored procedure calculates exposure (value × risk score) and ranks properties, with an optional risk category filter
- **AI risk segmentation:** K-Means clustering groups properties into low, medium, and high risk tiers based on value and risk score
- **CSV import and export** with pandas
- **Input validation:** invalid IDs, values, scores, and categories are rejected without crashing
- **Automated testing:** unit tests run on every push through GitHub Actions

## Tech Stack

| Area | Tools |
|---|---|
| Language | Python |
| Database | MS SQL Server, T-SQL |
| Database connection | pyodbc (ODBC Driver 18 for SQL Server) |
| Data and ML | pandas, scikit-learn |
| Testing and CI | unittest, GitHub Actions |

## Database Design

The schema is normalized into three tables linked by foreign keys:

| Table | Holds | Links to |
|---|---|---|
| `risk_categories` | Each risk type (Fire, Flood, and so on), stored once | none |
| `properties` | Property name and location | `risk_categories` |
| `valuations` | Property value and risk score | `properties` |

Storing each category once prevents duplicates and misspellings, and foreign keys stop a property from pointing to a category that doesn't exist.

### Stored procedure: `dbo.usp_RankPropertyExposure`

Joins all three tables, calculates exposure, and ranks properties using the `RANK()` window function.

```sql
-- All properties, ranked by exposure
EXEC dbo.usp_RankPropertyExposure;

-- Only Flood properties
EXEC dbo.usp_RankPropertyExposure @RiskCategory = 'Flood';
```

### Transactions

Adding, updating, or deleting a property touches more than one table. Each change runs in a transaction: if any step fails, the whole change is rolled back, so a property can never exist without its valuation.

## Project Structure

```
Property-Risk-Tracker/
├── .github/workflows/tests.yml         # CI: runs unit tests on every push
├── 01_create_tables.sql                # Creates the three tables
├── 02_seed_data.sql                    # Loads sample data
├── 03_usp_RankPropertyExposure.sql     # Exposure ranking stored procedure
├── main.py                             # Command-line menu and ML segmentation
├── database.py                         # SQL Server data access with pyodbc
├── models.py                           # Property class
├── check_connection.py                 # Quick SQL Server connection check
├── test_models.py                      # Unit tests
└── requirements.txt
```

## Setup

### 1. Install prerequisites

- Python 3
- SQL Server Developer Edition (free for development)
- SQL Server Management Studio (SSMS)
- ODBC Driver 18 for SQL Server

### 2. Create the database

In SSMS, connect to `localhost` and run:

```sql
CREATE DATABASE PropertyRiskTracker;
```

Then run the scripts in order:

1. `01_create_tables.sql`
2. `02_seed_data.sql`
3. `03_usp_RankPropertyExposure.sql`

### 3. Install Python dependencies

```
pip install -r requirements.txt
```

### 4. Check the connection

```
python check_connection.py
```

You should see the two Flood properties ranked by exposure.

### 5. Run the app

```
python main.py
```

## Running Tests

```
python -m unittest discover -v
```

GitHub Actions runs these tests automatically on every push to `main`. The unit tests cover the `Property` model and don't require a database connection.

## Planned Improvements

- Add indexes and measure query performance on a larger dataset
- Expand test coverage to the data access layer
- Build a web interface with React and TypeScript