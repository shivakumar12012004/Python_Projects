import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import datahandling as dh
import Visuals as vis

CATEGORIES = ["Food", "Travel", "Bills", "Shopping", "Health", "Entertainment", "Salary", "Other"]
ACCOUNTS   = ["Cash", "UPI", "Credit Card", "Debit Card", "Bank Transfer", "Other"]
INC_EXP    = ["Expense", "Income"]

BG     = "#1e1e2e"
CARD   = "#2a2a3e"
ACCENT = "#7c6af7"
TEXT   = "#e0e0f0"
LIGHT  = "#a0a0c0"
GREEN  = "#4ecdc4"
RED    = "#ff6b6b"

def launch():
    dh.setup_file()
    root = tk.Tk()
    root.title("Smart Expense Tracker")
    root.geometry("760x640")
    root.configure(bg=BG)
    root.resizable(False, False)

    tk.Label(root, text="💸 Smart Expense Tracker",
             font=("Segoe UI", 18, "bold"), bg=BG, fg=ACCENT).pack(pady=(18, 3))
    tk.Label(root, text="Track your spending. Understand your habits.",
             font=("Segoe UI", 10), bg=BG, fg=LIGHT).pack(pady=(0, 12))

    style = ttk.Style()
    style.theme_use("default")
    style.configure("TNotebook", background=BG, borderwidth=0)
    style.configure("TNotebook.Tab", background=CARD, foreground=TEXT,
                    padding=[12, 6], font=("Segoe UI", 10))
    style.map("TNotebook.Tab",
              background=[("selected", ACCENT)],
              foreground=[("selected", "white")])
    style.configure("Treeview", background=CARD, foreground=TEXT,
                    fieldbackground=CARD, font=("Segoe UI", 10), rowheight=26)
    style.configure("Treeview.Heading", background=ACCENT, foreground="white",
                    font=("Segoe UI", 10, "bold"))
    style.map("Treeview", background=[("selected", "#5a4fd4")])

    tabs = ttk.Notebook(root)
    tabs.pack(fill="both", expand=True, padx=20, pady=8)

    add_tab     = tk.Frame(tabs, bg=BG)
    view_tab    = tk.Frame(tabs, bg=BG)
    summary_tab = tk.Frame(tabs, bg=BG)
    import_tab  = tk.Frame(tabs, bg=BG)

    tabs.add(add_tab,     text="  ➕ Add Expense  ")
    tabs.add(view_tab,    text="  📋 View Records  ")
    tabs.add(summary_tab, text="  📊 Monthly Summary  ")
    tabs.add(import_tab,  text="  📂 Import CSV  ")

    build_add_tab(add_tab)
    build_view_tab(view_tab)
    build_summary_tab(summary_tab)
    build_import_tab(import_tab)

    root.mainloop()


def make_label(parent, text):
    return tk.Label(parent, text=text, font=("Segoe UI", 10),
                    bg=CARD, fg=LIGHT, anchor="w")

def make_entry(parent):
    return tk.Entry(parent, font=("Segoe UI", 11),
                    bg="#3a3a5e", fg=TEXT, insertbackground=TEXT,
                    relief="flat", bd=6)

def make_combo(parent, var, values):
    style = ttk.Style()
    style.configure("TCombobox", fieldbackground="#3a3a5e",
                    background=CARD, foreground=TEXT)
    cb = ttk.Combobox(parent, textvariable=var, values=values,
                      font=("Segoe UI", 11), state="readonly")
    return cb


def build_add_tab(parent):
    frame = tk.Frame(parent, bg=CARD)
    frame.pack(padx=30, pady=18, fill="both", expand=True)

    make_label(frame, "📅  Date (YYYY-MM-DD)").pack(fill="x", padx=20, pady=(16, 2))
    date_entry = make_entry(frame)
    date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))
    date_entry.pack(fill="x", padx=20, pady=(0, 8))

    make_label(frame, "🏦  Account").pack(fill="x", padx=20, pady=(4, 2))
    acc_var = tk.StringVar(value=ACCOUNTS[0])
    make_combo(frame, acc_var, ACCOUNTS).pack(fill="x", padx=20, pady=(0, 8))

    make_label(frame, "🏷️  Category").pack(fill="x", padx=20, pady=(4, 2))
    cat_var = tk.StringVar(value=CATEGORIES[0])
    make_combo(frame, cat_var, CATEGORIES).pack(fill="x", padx=20, pady=(0, 8))

    make_label(frame, "🔄  Type").pack(fill="x", padx=20, pady=(4, 2))
    ie_var = tk.StringVar(value="Expense")
    make_combo(frame, ie_var, INC_EXP).pack(fill="x", padx=20, pady=(0, 8))

    make_label(frame, "💰  Amount (₹)").pack(fill="x", padx=20, pady=(4, 2))
    amount_entry = make_entry(frame)
    amount_entry.pack(fill="x", padx=20, pady=(0, 16))

    status = tk.Label(frame, text="", font=("Segoe UI", 10), bg=CARD)
    status.pack()

    def save():
        date   = date_entry.get().strip()
        acc    = acc_var.get()
        cat    = cat_var.get()
        ie     = ie_var.get()
        amount = amount_entry.get().strip()

        if not date or not amount:
            status.config(text="Please fill Date and Amount!", fg=RED)
            return
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except:
            status.config(text="Date format must be YYYY-MM-DD", fg=RED)
            return
        try:
            float(amount)
        except:
            status.config(text="Amount must be a number.", fg=RED)
            return

        dh.save_expense(date, acc, cat, ie, float(amount))
        status.config(text=f"✅ Saved! ₹{amount} — {cat} ({ie})", fg=GREEN)
        amount_entry.delete(0, tk.END)

    tk.Button(frame, text="  Save  ", font=("Segoe UI", 11, "bold"),
              bg=ACCENT, fg="white", relief="flat", cursor="hand2",
              command=save, padx=14, pady=6).pack(pady=4)


def build_view_tab(parent):
    frame = tk.Frame(parent, bg=BG)
    frame.pack(fill="both", expand=True, padx=16, pady=10)

    cols = ("Date", "Account", "Category", "Type", "Amount")
    tree = ttk.Treeview(frame, columns=cols, show="headings", height=16)

    widths = {"Date": 110, "Account": 130, "Category": 140, "Type": 100, "Amount": 110}
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=widths[col], anchor="center")

    sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sb.set)
    tree.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")

    def refresh():
        for row in tree.get_children():
            tree.delete(row)
        df = dh.load_all()
        for _, row in df.iloc[::-1].iterrows():
            tree.insert("", "end", values=(
                str(row["Date"])[:10],
                row["Account"],
                row["Category"],
                row["Income/Expense"],
                f"₹{row['Amount']:.2f}"
            ))

    refresh()
    tk.Button(parent, text="🔄 Refresh", font=("Segoe UI", 10),
              bg=CARD, fg=TEXT, relief="flat", cursor="hand2",
              command=refresh, padx=8, pady=4).pack(pady=6)


def build_summary_tab(parent):
    frame = tk.Frame(parent, bg=BG)
    frame.pack(fill="both", expand=True, padx=20, pady=10)

    top = tk.Frame(frame, bg=BG)
    top.pack(fill="x", pady=8)

    tk.Label(top, text="Month (1-12):", font=("Segoe UI", 10), bg=BG, fg=LIGHT).pack(side="left", padx=(0, 4))
    month_var = tk.StringVar(value=str(datetime.today().month))
    tk.Entry(top, textvariable=month_var, width=5, font=("Segoe UI", 11),
             bg="#3a3a5e", fg=TEXT, insertbackground=TEXT,
             relief="flat", bd=4).pack(side="left", padx=4)

    tk.Label(top, text="Year:", font=("Segoe UI", 10), bg=BG, fg=LIGHT).pack(side="left", padx=(10, 4))
    year_var = tk.StringVar(value=str(datetime.today().year))
    tk.Entry(top, textvariable=year_var, width=7, font=("Segoe UI", 11),
             bg="#3a3a5e", fg=TEXT, insertbackground=TEXT,
             relief="flat", bd=4).pack(side="left", padx=4)

    info_box = tk.Text(frame, font=("Courier New", 10), bg=CARD, fg=TEXT,
                       relief="flat", height=12, padx=12, pady=10)
    info_box.pack(fill="both", expand=True, pady=8)

    def get_m_y():
        try:
            return int(month_var.get()), int(year_var.get())
        except:
            messagebox.showerror("Error", "Enter a valid month and year.")
            return None, None

    def show_summary():
        m, y = get_m_y()
        if m is None:
            return
        df = dh.get_month_data(m, y)
        totals = dh.get_category_totals(df)
        income = dh.get_income_total(df)
        top_cat, top_amt = dh.get_highest_category(totals)
        total_exp = sum(totals.values())

        info_box.config(state="normal")
        info_box.delete("1.0", tk.END)

        if df.empty:
            info_box.insert(tk.END, f"No records found for {m}/{y}.\n")
        else:
            info_box.insert(tk.END, f"  Summary — {m}/{y}\n")
            info_box.insert(tk.END, "  " + "─" * 36 + "\n\n")
            for cat, amt in sorted(totals.items(), key=lambda x: x[1], reverse=True):
                bar = "█" * int(amt / max(totals.values()) * 20)
                info_box.insert(tk.END, f"  {cat:<18} ₹{amt:>8.2f}  {bar}\n")
            info_box.insert(tk.END, "\n  " + "─" * 36 + "\n")
            info_box.insert(tk.END, f"  Total Expense :  ₹{total_exp:.2f}\n")
            info_box.insert(tk.END, f"  Total Income  :  ₹{income:.2f}\n")
            info_box.insert(tk.END, f"  Net Balance   :  ₹{income - total_exp:.2f}\n\n")
            if top_cat:
                info_box.insert(tk.END, f"  🔺 Highest Spend: {top_cat} (₹{top_amt:.2f})\n")
                info_box.insert(tk.END, f"  💡 Tip: Try cutting down on {top_cat} expenses!\n")

        info_box.config(state="disabled")

    def show_pie():
        m, y = get_m_y()
        if m is None:
            return
        df = dh.get_month_data(m, y)
        vis.show_pie_chart(dh.get_category_totals(df), m, y)

    def show_bar():
        m, y = get_m_y()
        if m is None:
            return
        df = dh.get_month_data(m, y)
        vis.show_bar_chart(dh.get_category_totals(df), m, y)

    def show_inc_exp():
        m, y = get_m_y()
        if m is None:
            return
        df = dh.get_month_data(m, y)
        income  = dh.get_income_total(df)
        expense = sum(dh.get_category_totals(df).values())
        vis.show_income_vs_expense(income, expense, m, y)

    btn_row = tk.Frame(frame, bg=BG)
    btn_row.pack(pady=4)

    def btn(text, cmd, color):
        return tk.Button(btn_row, text=text, font=("Segoe UI", 10, "bold"),
                         bg=color, fg="white", relief="flat", cursor="hand2",
                         command=cmd, padx=10, pady=6)

    btn("📋 Summary",       show_summary,  ACCENT).pack(side="left", padx=5)
    btn("🥧 Pie Chart",     show_pie,      "#e07b54").pack(side="left", padx=5)
    btn("📊 Bar Chart",     show_bar,      GREEN).pack(side="left", padx=5)
    btn("💹 Income/Expense", show_inc_exp, "#f0a500").pack(side="left", padx=5)


def build_import_tab(parent):
    frame = tk.Frame(parent, bg=CARD)
    frame.pack(padx=40, pady=30, fill="both", expand=True)

    tk.Label(frame, text="📂  Import Expenses from CSV",
             font=("Segoe UI", 13, "bold"), bg=CARD, fg=ACCENT).pack(pady=(20, 6))

    tk.Label(frame,
             text="Your CSV must have these columns:\nDate  |  Account  |  Category  |  Income/Expense  |  Amount",
             font=("Segoe UI", 10), bg=CARD, fg=LIGHT, justify="center").pack(pady=(0, 20))

    file_var = tk.StringVar(value="No file selected")
    file_label = tk.Label(frame, textvariable=file_var, font=("Segoe UI", 10),
                          bg="#3a3a5e", fg=TEXT, padx=10, pady=6, anchor="w")
    file_label.pack(fill="x", padx=20, pady=(0, 10))

    status = tk.Label(frame, text="", font=("Segoe UI", 10), bg=CARD)
    status.pack()

    chosen_path = {"path": None}

    def browse():
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if path:
            chosen_path["path"] = path
            file_var.set(path)
            status.config(text="")

    def do_import():
        if not chosen_path["path"]:
            status.config(text="Please select a CSV file first.", fg=RED)
            return
        ok, msg = dh.import_from_csv(chosen_path["path"])
        if ok:
            status.config(text=f"✅ {msg}", fg=GREEN)
        else:
            status.config(text=f"❌ {msg}", fg=RED)

    tk.Button(frame, text="📁  Browse File", font=("Segoe UI", 11),
              bg="#3a3a5e", fg=TEXT, relief="flat", cursor="hand2",
              command=browse, padx=10, pady=6).pack(pady=6)

    tk.Button(frame, text="⬆️  Import into Tracker", font=("Segoe UI", 11, "bold"),
              bg=ACCENT, fg="white", relief="flat", cursor="hand2",
              command=do_import, padx=12, pady=7).pack(pady=6)