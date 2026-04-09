import pandas as pd
import os
from datetime import datetime

FILE = "Data/expense_data.csv"

def setup_file():
    if not os.path.exists(FILE):
        os.makedirs("Data", exist_ok=True)
        df = pd.DataFrame(columns=["Date", "Account", "Category", "Income/Expense", "Amount"])
        df.to_csv(FILE, index=False)

def load_clean():
    df = pd.read_csv(FILE)

    df.dropna(axis=1, how="all", inplace=True)

    if "INR" in df.columns:
        df.drop("INR", axis=1, inplace=True)

    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df.dropna(subset=["Amount"], inplace=True)

    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    df.dropna(subset=["Date"], inplace=True)

    return df

def print_info():
    df = load_clean()
    print(df.info())
    print(df.describe())

def save_expense(date, account, category, inc_exp, amount):
    df = pd.read_csv(FILE)
    new_row = {
        "Date": date,
        "Account": account,
        "Category": category,
        "Income/Expense": inc_exp,
        "Amount": float(amount)
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(FILE, index=False)

def import_from_csv(filepath):
    try:
        incoming = pd.read_csv(filepath)
    except Exception as e:
        return False, str(e)

    incoming.dropna(axis=1, how="all", inplace=True)

    if "INR" in incoming.columns:
        incoming.drop("INR", axis=1, inplace=True)

    needed = ["Date", "Account", "Category", "Income/Expense", "Amount"]
    for col in needed:
        if col not in incoming.columns:
            return False, f"Missing column: '{col}' — make sure your CSV has: {needed}"

    existing = pd.read_csv(FILE)
    merged = pd.concat([existing, incoming], ignore_index=True)
    merged.drop_duplicates(inplace=True)
    merged.to_csv(FILE, index=False)
    return True, f"Imported {len(incoming)} rows successfully."

def load_all():
    return load_clean()

def get_month_data(month, year):
    df = load_clean()
    filtered = df[(df["Date"].dt.month == month) & (df["Date"].dt.year == year)]
    return filtered

def get_expenses_only(df):
    return df[df["Income/Expense"].str.strip().str.lower() == "expense"]

def get_category_totals(df):
    expenses = get_expenses_only(df)
    totals = expenses.groupby("Category")["Amount"].sum().to_dict()
    return totals

def get_income_total(df):
    income = df[df["Income/Expense"].str.strip().str.lower() == "income"]
    return income["Amount"].sum()

def get_highest_category(totals):
    if not totals:
        return None, 0
    top = max(totals, key=totals.get)
    return top, totals[top]