import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from datetime import datetime
from datahandling import (getdf, cleandf, get_monthly_totals, get_category_analysis, 
                          get_weekly_expense_income, get_monthly_expense_income, gettotalamount)
from Visuals import (plot_category_pie_chart, plot_monthly_totals_bar, plot_category_analysis_bar,
                    plot_weekly_expense_income_line, plot_monthly_expense_income_line,
                    plot_monthly_expense_income_grouped_bar, plot_category_income_expense_comparison)

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        self.file_path = "Data/expense_data.csv"
        self.df = getdf(self.file_path)
        cleandf(self.df)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.add_data_tab()
        self.analysis_tab()
        self.summary_tab()
        
    def add_data_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Add Data")
        title = tk.Label(frame, text="Add New Transaction", font=("Arial", 14, "bold"))
        title.pack(pady=10)
        form_frame = tk.Frame(frame, bg="white")
        form_frame.pack(padx=20, pady=10, fill=tk.BOTH)
        tk.Label(form_frame, text="Date (DD-MM-YYYY):", bg="white", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=8)
        self.date_entry = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.date_entry.insert(0, datetime.now().strftime("%d-%m-%Y"))
        self.date_entry.grid(row=0, column=1, pady=8)
        tk.Label(form_frame, text="Account:", bg="white", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=8)
        self.account_entry = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.account_entry.grid(row=1, column=1, pady=8)
        tk.Label(form_frame, text="Category:", bg="white", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=8)
        self.category_var = tk.StringVar()
        categories = ["Food", "Transportation", "Household", "Social Life", "Other"]
        category_combo = ttk.Combobox(form_frame, textvariable=self.category_var, values=categories, font=("Arial", 10), state="readonly", width=27)
        category_combo.grid(row=2, column=1, pady=8)
        tk.Label(form_frame, text="Note/Description:", bg="white", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=8)
        self.note_entry = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.note_entry.grid(row=3, column=1, pady=8)
        tk.Label(form_frame, text="Type:", bg="white", font=("Arial", 10)).grid(row=4, column=0, sticky="w", pady=8)
        self.type_var = tk.StringVar(value="Expense")
        type_combo = ttk.Combobox(form_frame, textvariable=self.type_var, values=["Income", "Expense"], font=("Arial", 10), state="readonly", width=27)
        type_combo.grid(row=4, column=1, pady=8)
        tk.Label(form_frame, text="Amount (₹):", bg="white", font=("Arial", 10)).grid(row=5, column=0, sticky="w", pady=8)
        self.amount_entry = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.amount_entry.grid(row=5, column=1, pady=8)
        button_frame = tk.Frame(frame, bg="white")
        button_frame.pack(pady=20)
        add_btn = tk.Button(button_frame, text="Add Transaction", font=("Arial", 11, "bold"), 
                           bg="#4CAF50", fg="white", padx=15, pady=8, command=self.add_transaction)
        add_btn.pack(side=tk.LEFT, padx=5)
        refresh_btn = tk.Button(button_frame, text="Refresh Data", font=("Arial", 11, "bold"), 
                               bg="#2196F3", fg="white", padx=15, pady=8, command=self.refresh_data)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
    def analysis_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Analysis")
        title = tk.Label(frame, text="Financial Analysis", font=("Arial", 14, "bold"))
        title.pack(pady=10)
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10, fill=tk.X, padx=10)
        graph_buttons = [
            ("Category Expenses", plot_category_pie_chart),
            ("Monthly Totals", plot_monthly_totals_bar),
            ("Category Analysis", plot_category_analysis_bar),
            ("Weekly Trend", plot_weekly_expense_income_line),
        ]
        for i, (label, func) in enumerate(graph_buttons):
            btn = tk.Button(button_frame, text=label, font=("Arial", 10), 
                           bg="#FF9800", fg="white", padx=12, pady=6, command=func)
            btn.pack(side=tk.LEFT, padx=5, pady=5)
        button_frame2 = tk.Frame(frame)
        button_frame2.pack(pady=5, fill=tk.X, padx=10)
        graph_buttons2 = [
            ("Monthly Trend", plot_monthly_expense_income_line),
            ("Monthly Comparison", plot_monthly_expense_income_grouped_bar),
            ("Category Breakdown", plot_category_income_expense_comparison),
        ]
        for label, func in graph_buttons2:
            btn = tk.Button(button_frame2, text=label, font=("Arial", 10), 
                           bg="#FF9800", fg="white", padx=12, pady=6, command=func)
            btn.pack(side=tk.LEFT, padx=5, pady=5)
        info_text = tk.Text(frame, height=15, width=100, font=("Arial", 10), bg="#f0f0f0")
        info_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(info_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        info_text['yscrollcommand'] = scrollbar.set
        scrollbar['command'] = info_text.yview
        self.display_analysis(info_text)
        
    def summary_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Summary")
        title = tk.Label(frame, text="Financial Summary", font=("Arial", 14, "bold"))
        title.pack(pady=10)
        summary_frame = tk.Frame(frame, bg="white", relief=tk.SUNKEN, bd=2)
        summary_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        monthly_data = get_monthly_expense_income(self.df)
        category_data = get_category_analysis(self.df)
        summary_text = tk.Text(summary_frame, height=25, width=100, font=("Arial", 10), bg="white")
        summary_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        summary_text.insert(tk.END, "=" * 80 + "\n", "header")
        summary_text.insert(tk.END, "EXPENSE TRACKER SUMMARY\n", "header")
        summary_text.insert(tk.END, "=" * 80 + "\n\n", "header")
        summary_text.insert(tk.END, "MONTHLY BREAKDOWN:\n", "bold")
        summary_text.insert(tk.END, "-" * 80 + "\n")
        total_expenses = 0
        total_income = 0
        for month, data in sorted(monthly_data.items()):
            expenses = data['expenses']
            income = data['income']
            net = data['net']
            total_expenses += expenses
            total_income += income
            summary_text.insert(tk.END, f"{month:20} | Income: ₹{income:10.2f} | Expenses: ₹{expenses:10.2f} | Net: ₹{net:10.2f}\n")
        summary_text.insert(tk.END, "-" * 80 + "\n")
        summary_text.insert(tk.END, f"{'TOTAL':20} | Income: ₹{total_income:10.2f} | Expenses: ₹{total_expenses:10.2f} | Net: ₹{total_income - total_expenses:10.2f}\n\n")
        summary_text.insert(tk.END, "CATEGORY-WISE BREAKDOWN:\n", "bold")
        summary_text.insert(tk.END, "-" * 80 + "\n")
        for category, data in sorted(category_data.items()):
            summary_text.insert(tk.END, f"{category:20} | Expenses: ₹{data['expenses']:10.2f} | Income: ₹{data['income']:10.2f} | Transactions: {data['transaction_count']}\n")
        summary_text.insert(tk.END, "\n" + "=" * 80 + "\n")
        if total_expenses > total_income:
            summary_text.insert(tk.END, "⚠️  WARNING: Your expenses are more than income!\n", "warning")
            summary_text.insert(tk.END, "💡 Tip: Reduce or adjust your expenses. Do not spend unnecessarily!\n", "warning")
            summary_text.insert(tk.END, f"   Excess Amount: ₹{total_expenses - total_income:.2f}\n", "warning")
        else:
            summary_text.insert(tk.END, "✓ Great! Your income is higher than expenses.\n", "success")
            summary_text.insert(tk.END, f"  Savings: ₹{total_income - total_expenses:.2f}\n", "success")
        summary_text.insert(tk.END, "=" * 80 + "\n")
        summary_text.tag_config("header", font=("Arial", 12, "bold"), foreground="#1976D2")
        summary_text.tag_config("bold", font=("Arial", 11, "bold"))
        summary_text.tag_config("warning", font=("Arial", 10, "bold"), foreground="#D32F2F", background="#FFEBEE")
        summary_text.tag_config("success", font=("Arial", 10, "bold"), foreground="#388E3C", background="#E8F5E9")
        summary_text.config(state=tk.DISABLED)
        
    def display_analysis(self, text_widget):
        monthly_data = get_monthly_expense_income(self.df)
        weekly_data = get_weekly_expense_income(self.df)
        category_data = get_category_analysis(self.df)
        text_widget.insert(tk.END, "=" * 100 + "\n")
        text_widget.insert(tk.END, "MONTHLY ANALYSIS\n", "bold")
        text_widget.insert(tk.END, "=" * 100 + "\n\n")
        for month, data in sorted(monthly_data.items()):
            text_widget.insert(tk.END, f"{month}:\n")
            text_widget.insert(tk.END, f"  Income:    ₹{data['income']:10.2f}\n")
            text_widget.insert(tk.END, f"  Expenses:  ₹{data['expenses']:10.2f}\n")
            text_widget.insert(tk.END, f"  Net:       ₹{data['net']:10.2f}\n\n")
        text_widget.insert(tk.END, "=" * 100 + "\n")
        text_widget.insert(tk.END, "WEEKLY ANALYSIS\n", "bold")
        text_widget.insert(tk.END, "=" * 100 + "\n\n")
        for week, data in sorted(weekly_data.items()):
            text_widget.insert(tk.END, f"{week}:\n")
            text_widget.insert(tk.END, f"  Income:    ₹{data['income']:10.2f}\n")
            text_widget.insert(tk.END, f"  Expenses:  ₹{data['expenses']:10.2f}\n")
            text_widget.insert(tk.END, f"  Net:       ₹{data['net']:10.2f}\n\n")
        text_widget.insert(tk.END, "=" * 100 + "\n")
        text_widget.insert(tk.END, "CATEGORY ANALYSIS\n", "bold")
        text_widget.insert(tk.END, "=" * 100 + "\n\n")
        for category, data in sorted(category_data.items()):
            text_widget.insert(tk.END, f"{category}:\n")
            text_widget.insert(tk.END, f"  Total:         ₹{data['total']:10.2f}\n")
            text_widget.insert(tk.END, f"  Expenses:      ₹{data['expenses']:10.2f}\n")
            text_widget.insert(tk.END, f"  Income:        ₹{data['income']:10.2f}\n")
            text_widget.insert(tk.END, f"  Transactions:  {data['transaction_count']}\n\n")
        text_widget.config(state=tk.DISABLED)
        
    def add_transaction(self):
        try:
            date = self.date_entry.get()
            account = self.account_entry.get()
            category = self.category_var.get()
            note = self.note_entry.get()
            trans_type = self.type_var.get()
            amount = float(self.amount_entry.get())
            if not all([date, account, category, trans_type, amount]):
                messagebox.showerror("Error", "Please fill all required fields!")
                return
            new_row = {
                'Date': date,
                'Account': account,
                'Category': category,
                'Subcategory': '',
                'Note': note,
                'INR': amount,
                'Income/Expense': trans_type,
                'Note.1': '',
                'Amount': amount
            }
            self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
            self.df.to_csv(self.file_path, index=False)
            messagebox.showinfo("Success", "Transaction added successfully!")
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, datetime.now().strftime("%d-%m-%Y"))
            self.account_entry.delete(0, tk.END)
            self.category_var.set('')
            self.note_entry.delete(0, tk.END)
            self.type_var.set("Expense")
            self.amount_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount! Please enter a number.")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding transaction: {str(e)}")
    
    def refresh_data(self):
        try:
            self.df = getdf(self.file_path)
            cleandf(self.df)
            messagebox.showinfo("Success", "Data refreshed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error refreshing data: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
