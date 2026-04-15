# Smart Expense Tracker 💸

A beginner-friendly Python desktop app to log, import, and analyse your daily expenses.

## How to Run

1. Install required libraries:
```
pip install pandas matplotlib
```

2. Run the app:
```
python main.py
```

## CSV Format

Your `expense_data.csv` (or any CSV you import) must have exactly these columns:

| Column | Example |
|--------|---------|
| Date | 2024-03-15 |
| Account | UPI / Cash / Credit Card |
| Category | Food / Travel / Bills … |
| Income/Expense | Expense or Income |
| Amount | 250.0 |

> If your CSV has an extra `INR` column, it gets dropped automatically.

## Features

| Tab | What it does |
|-----|-------------|
| ➕ Add Expense | Manually enter a record |
| 📋 View Records | See all entries in a table |
| 📊 Monthly Summary | Text summary + 3 chart types |
| 📂 Import CSV | Load an existing CSV into the tracker |

## Charts Available
- 🥧 Pie chart — category breakdown
- 📊 Bar chart — category spending bars
- 💹 Income vs Expense — side-by-side comparison

## Files

``` 
├── main.py           ← run this
├── datahandling.py   ← pandas data logic
├── Visuals.py        ← matplotlib charts
└── Data/ expense_data.csv  ← your data lives here
```
