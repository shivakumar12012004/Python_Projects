import matplotlib.pyplot as plt
from datahandling import (getdf, cleandf, get_monthly_totals, 
                          get_category_analysis, get_weekly_expense_income, get_monthly_expense_income)

# Load and clean data
df = getdf("Data/expense_data.csv")
cleandf(df)

def plot_category_pie_chart():
    category_analysis = get_category_analysis(df)
    categories = list(category_analysis.keys())
    expenses = [category_analysis[cat]['expenses'] for cat in categories]
    plt.figure(figsize=(10, 8))
    colors = plt.cm.Set3(range(len(categories)))
    wedges, texts, autotexts = plt.pie(expenses, labels=categories, autopct='%1.1f%%',
                                         colors=colors, startangle=90)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    plt.title('Category-wise Expense Distribution', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

def plot_monthly_totals_bar():
    monthly_totals = get_monthly_totals(df)
    months = list(monthly_totals.keys())
    amounts = list(monthly_totals.values())
    plt.figure(figsize=(14, 6))
    bars = plt.bar(months, amounts, color='steelblue', alpha=0.8, edgecolor='navy')
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'₹{height:.0f}', ha='center', va='bottom', fontweight='bold')

    plt.xlabel('Month', fontsize=12, fontweight='bold')
    plt.ylabel('Total Amount (₹)', fontsize=12, fontweight='bold')
    plt.title('Monthly Total Transaction Amount', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_category_analysis_bar():
    category_analysis = get_category_analysis(df)
    categories = list(category_analysis.keys())
    expenses = [category_analysis[cat]['expenses'] for cat in categories]
    plt.figure(figsize=(12, 6))
    bars = plt.bar(categories, expenses, color='coral', alpha=0.8, edgecolor='darkred')    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'₹{height:.0f}', ha='center', va='bottom', fontweight='bold', fontsize=10)
    plt.xlabel('Category', fontsize=12, fontweight='bold')
    plt.ylabel('Expenses (₹)', fontsize=12, fontweight='bold')
    plt.title('Category-wise Expense Amount', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_weekly_expense_income_line():
    weekly_data = get_weekly_expense_income(df)
    weeks = list(weekly_data.keys())
    expenses = [weekly_data[week]['expenses'] for week in weeks]
    income = [weekly_data[week]['income'] for week in weeks]
    plt.figure(figsize=(14, 6))
    plt.plot(weeks, expenses, marker='o', linewidth=2, markersize=8, 
             label='Expenses', color='red', alpha=0.7)
    plt.plot(weeks, income, marker='s', linewidth=2, markersize=8, 
             label='Income', color='green', alpha=0.7)
    plt.xlabel('Week', fontsize=12, fontweight='bold')
    plt.ylabel('Amount (₹)', fontsize=12, fontweight='bold')
    plt.title('Weekly Expense vs Income Trend', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.xticks(rotation=45)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_monthly_expense_income_line():
    monthly_data = get_monthly_expense_income(df)
    months = list(monthly_data.keys())
    expenses = [monthly_data[month]['expenses'] for month in months]
    income = [monthly_data[month]['income'] for month in months]
    net = [monthly_data[month]['net'] for month in months]
    plt.figure(figsize=(14, 6))
    plt.plot(months, expenses, marker='o', linewidth=2.5, markersize=8, 
             label='Expenses', color='#e74c3c', alpha=0.8)
    plt.plot(months, income, marker='s', linewidth=2.5, markersize=8, 
             label='Income', color='#27ae60', alpha=0.8)
    plt.plot(months, net, marker='^', linewidth=2.5, markersize=8, 
             label='Net Balance', color='#3498db', alpha=0.8)
    plt.xlabel('Month', fontsize=12, fontweight='bold')
    plt.ylabel('Amount (₹)', fontsize=12, fontweight='bold')
    plt.title('Monthly Expense vs Income vs Net Balance Trend', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.xticks(rotation=45)
    plt.grid(alpha=0.3)
    plt.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
    plt.tight_layout()
    plt.show()

def plot_monthly_expense_income_grouped_bar():
    monthly_data = get_monthly_expense_income(df)
    months = list(monthly_data.keys())
    expenses = [monthly_data[month]['expenses'] for month in months]
    income = [monthly_data[month]['income'] for month in months]
    x = range(len(months))
    width = 0.35
    plt.figure(figsize=(14, 6))
    bars1 = plt.bar([i - width/2 for i in x], expenses, width, label='Expenses', 
                     color='#e74c3c', alpha=0.8, edgecolor='darkred')
    bars2 = plt.bar([i + width/2 for i in x], income, width, label='Income', 
                     color='#27ae60', alpha=0.8, edgecolor='darkgreen')    
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'₹{height:.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    plt.xlabel('Month', fontsize=12, fontweight='bold')
    plt.ylabel('Amount (₹)', fontsize=12, fontweight='bold')
    plt.title('Monthly Expenses vs Income Comparison', fontsize=14, fontweight='bold')
    plt.xticks([i for i in x], months, rotation=45)
    plt.legend(fontsize=11)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_category_income_expense_comparison():
    category_analysis = get_category_analysis(df)
    categories = list(category_analysis.keys())
    expenses = [category_analysis[cat]['expenses'] for cat in categories]
    income = [category_analysis[cat]['income'] for cat in categories]
    x = range(len(categories))
    width = 0.35
    plt.figure(figsize=(13, 6))
    bars1 = plt.bar([i - width/2 for i in x], expenses, width, label='Expenses', 
                     color='#e74c3c', alpha=0.8, edgecolor='darkred')
    bars2 = plt.bar([i + width/2 for i in x], income, width, label='Income', 
                     color='#27ae60', alpha=0.8, edgecolor='darkgreen')
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'₹{height:.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.xlabel('Category', fontsize=12, fontweight='bold')
    plt.ylabel('Amount (₹)', fontsize=12, fontweight='bold')
    plt.title('Category-wise Income vs Expense Breakdown', fontsize=14, fontweight='bold')
    plt.xticks([i for i in x], categories, rotation=45)
    plt.legend(fontsize=11)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

def show_all_visualizations():
    """Display all visualizations"""
    print("Generating visualizations...")
    print("\n1. Category-wise Expense Distribution (Pie Chart)")
    plot_category_pie_chart()
    
    print("\n2. Monthly Total Transactions (Bar Chart)")
    plot_monthly_totals_bar()
    
    print("\n3. Category-wise Expenses (Bar Chart)")
    plot_category_analysis_bar()
    
    print("\n4. Weekly Expense vs Income Trend (Line Graph)")
    plot_weekly_expense_income_line()
    
    print("\n5. Monthly Expense vs Income Trend (Line Graph)")
    plot_monthly_expense_income_line()
    
    print("\n6. Monthly Expenses vs Income Comparison (Grouped Bar Chart)")
    plot_monthly_expense_income_grouped_bar()
    
    print("\n7. Category-wise Income vs Expense (Grouped Bar Chart)")
    plot_category_income_expense_comparison()

if __name__ == "__main__":
    show_all_visualizations()
