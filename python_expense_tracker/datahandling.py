import pandas as pd
from datetime import datetime

def getdf(file_loc):
    df = pd.read_csv(file_loc)
    df['Date'] = pd.to_datetime(df['Date'], format='%m-%d-%Y %H.%M', errors='coerce')
    df['Date'].fillna(pd.to_datetime(df['Date'], format='%m/%d/%Y %H:%M', errors='coerce'), inplace=True)
    return df

def getinfo(df):
    return df.info()

def cleandf(df):
    df.dropna(axis=1)
    df.drop(columns="INR", axis=1)

def gettotalamount(df):
    totalAmount = sum(df["Amount"])
    return totalAmount

def get_monthly_totals(df):
    df['YearMonth'] = df['Date'].dt.to_period('M')
    monthly_totals = df.groupby('YearMonth')['Amount'].sum().to_dict()
    return {str(k): v for k, v in monthly_totals.items()}

def get_category_analysis(df):
    category_analysis = {}
    for category in df['Category'].unique():
        category_df = df[df['Category'] == category]
        total = category_df['Amount'].sum()
        expenses = category_df[category_df['Income/Expense'] == 'Expense']['Amount'].sum()
        income = category_df[category_df['Income/Expense'] == 'Income']['Amount'].sum()
        count = len(category_df)   
        category_analysis[category] = {
            'total': total,
            'expenses': expenses,
            'income': income,
            'transaction_count': count
        }
    return category_analysis

def get_weekly_expense_income(df):
    df['Week'] = df['Date'].dt.to_period('W')
    weekly_data = {}
    for week in df['Week'].unique():
        week_df = df[df['Week'] == week]
        expenses = week_df[week_df['Income/Expense'] == 'Expense']['Amount'].sum()
        income = week_df[week_df['Income/Expense'] == 'Income']['Amount'].sum()
        net = income - expenses
        weekly_data[str(week)] = {
            'expenses': expenses,
            'income': income,
            'net': net
        }
    return weekly_data

def get_monthly_expense_income(df):
    df['YearMonth'] = df['Date'].dt.to_period('M')
    monthly_data = {}
    for month in df['YearMonth'].unique():
        month_df = df[df['YearMonth'] == month]
        expenses = month_df[month_df['Income/Expense'] == 'Expense']['Amount'].sum()
        income = month_df[month_df['Income/Expense'] == 'Income']['Amount'].sum()
        net = income - expenses
        monthly_data[str(month)] = {
            'expenses': expenses,
            'income': income,
            'net': net
        }
    
    return monthly_data
