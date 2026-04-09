import matplotlib.pyplot as plt

def show_pie_chart(totals, month, year):
    if not totals:
        print("No expense data to show.")
        return

    categories = list(totals.keys())
    amounts = list(totals.values())
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD", "#98D8C8", "#F7DC6F", "#82E0AA"]

    plt.figure(figsize=(7, 7))
    plt.pie(amounts, labels=categories, autopct="%1.1f%%",
            colors=colors[:len(categories)], startangle=140)
    plt.title(f"Spending Breakdown — {month}/{year}", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()

def show_bar_chart(totals, month, year):
    if not totals:
        print("No expense data to show.")
        return

    categories = list(totals.keys())
    amounts = list(totals.values())

    plt.figure(figsize=(9, 5))
    bars = plt.bar(categories, amounts, color="#7c6af7", edgecolor="black")

    for bar, amt in zip(bars, amounts):
        plt.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + max(amounts) * 0.01,
                 f"₹{amt:.0f}", ha="center", fontsize=9)

    plt.title(f"Category-wise Spending — {month}/{year}", fontsize=14, fontweight="bold")
    plt.xlabel("Category")
    plt.ylabel("Amount (₹)")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.show()

def show_income_vs_expense(income, expense, month, year):
    labels = ["Income", "Expense"]
    values = [income, expense]
    colors = ["#4ECDC4", "#FF6B6B"]

    plt.figure(figsize=(5, 5))
    bars = plt.bar(labels, values, color=colors, edgecolor="black", width=0.4)

    for bar, val in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + max(values) * 0.01,
                 f"₹{val:.0f}", ha="center", fontsize=11, fontweight="bold")

    plt.title(f"Income vs Expense — {month}/{year}", fontsize=13, fontweight="bold")
    plt.ylabel("Amount (₹)")
    plt.tight_layout()
    plt.show()