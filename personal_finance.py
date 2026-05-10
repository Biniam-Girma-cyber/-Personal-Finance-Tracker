import json
import os
from datetime import datetime
from collections import defaultdict

DATA_FILE = "finance_data.json"

CATEGORIES = {
    "income":  ["Salary", "Freelance", "Investment", "Gift", "Other Income"],
    "expense": ["Food", "Transport", "Housing", "Health", "Entertainment", "Shopping", "Education", "Other Expense"],
}


 
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"transactions": [], "budgets": {}}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def header(title):
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)


def fmt_money(amount):
    return f"${amount:,.2f}"


def fmt_row(txn):
    sign  = "+" if txn["type"] == "income" else "-"
    color = "\033[92m" if txn["type"] == "income" else "\033[91m"
    reset = "\033[0m"
    return (f"  [{txn['id']:>3}] {txn['date']}  {txn['category']:<20} "
            f"{txn['description']:<25} {color}{sign}{fmt_money(txn['amount'])}{reset}")


def add_transaction(data):
    header("Add Transaction")

    
    print("\n  Type:")
    print("  1. Income")
    print("  2. Expense")
    choice = input("\n  Choose (1/2): ").strip()
    if choice not in ("1", "2"):
        print("  Invalid choice.")
        return
    txn_type = "income" if choice == "1" else "expense"


    cats = CATEGORIES[txn_type]
    print(f"\n  Categories:")
    for i, c in enumerate(cats, 1):
        print(f"  {i}. {c}")
    cat_choice = input("\n  Choose category number: ").strip()
    if not cat_choice.isdigit() or not (1 <= int(cat_choice) <= len(cats)):
        print("  Invalid category.")
        return
    category = cats[int(cat_choice) - 1]

    description = input("\n  Description: ").strip()
    if not description:
        print("  Description cannot be empty.")
        return

    try:
        amount = float(input("\n  Amount ($): ").strip())
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("  Invalid amount.")
        return

    date_input = input("\n  Date (YYYY-MM-DD) [leave blank for today]: ").strip()
    if not date_input:
        date_input = datetime.today().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            print("  Invalid date format.")
            return

    txn_id = (max((t["id"] for t in data["transactions"]), default=0)) + 1
    txn = {
        "id":          txn_id,
        "type":        txn_type,
        "category":    category,
        "description": description,
        "amount":      round(amount, 2),
        "date":        date_input,
    }
    data["transactions"].append(txn)
    save_data(data)

    sign = "+" if txn_type == "income" else "-"
    print(f"\n  ✓ Transaction #{txn_id} saved: {sign}{fmt_money(amount)} ({category})")
    input("\n  Press Enter to continue...")


def view_transactions(data):
    header("All Transactions")

    txns = sorted(data["transactions"], key=lambda t: t["date"], reverse=True)
    if not txns:
        print("\n  No transactions yet.")
    else:
        print(f"\n  {'ID':>5}  {'Date':<12}  {'Category':<20}  {'Description':<25}  {'Amount'}")
        print("  " + "-" * 80)
        for t in txns:
            print(fmt_row(t))

    income  = sum(t["amount"] for t in txns if t["type"] == "income")
    expense = sum(t["amount"] for t in txns if t["type"] == "expense")
    balance = income - expense

    print("\n  " + "-" * 80)
    print(f"  \033[92mTotal Income : {fmt_money(income)}\033[0m")
    print(f"  \033[91mTotal Expense: {fmt_money(expense)}\033[0m")
    bal_color = "\033[92m" if balance >= 0 else "\033[91m"
    print(f"  {bal_color}Balance      : {fmt_money(balance)}\033[0m")
    input("\n  Press Enter to continue...")


def delete_transaction(data):
    header("Delete Transaction")

    txns = data["transactions"]
    if not txns:
        print("\n  No transactions to delete.")
        input("\n  Press Enter to continue...")
        return

    for t in sorted(txns, key=lambda x: x["date"], reverse=True):
        print(fmt_row(t))

    try:
        tid = int(input("\n  Enter transaction ID to delete: ").strip())
    except ValueError:
        print("  Invalid ID.")
        input("\n  Press Enter to continue...")
        return

    match = next((t for t in txns if t["id"] == tid), None)
    if not match:
        print(f"  No transaction with ID {tid}.")
    else:
        confirm = input(f"\n  Delete '{match['description']}' ({fmt_money(match['amount'])})? (y/n): ").strip().lower()
        if confirm == "y":
            data["transactions"] = [t for t in txns if t["id"] != tid]
            save_data(data)
            print("  ✓ Transaction deleted.")
        else:
            print("  Cancelled.")
    input("\n  Press Enter to continue...")


def monthly_report(data):
    header("Monthly Report")

    if not data["transactions"]:
        print("\n  No transactions yet.")
        input("\n  Press Enter to continue...")
        return

    month_input = input("\n  Enter month (YYYY-MM) [blank = current month]: ").strip()
    if not month_input:
        month_input = datetime.today().strftime("%Y-%m")

    txns = [t for t in data["transactions"] if t["date"].startswith(month_input)]
    if not txns:
        print(f"\n  No transactions found for {month_input}.")
        input("\n  Press Enter to continue...")
        return

    income_by_cat  = defaultdict(float)
    expense_by_cat = defaultdict(float)

    for t in txns:
        if t["type"] == "income":
            income_by_cat[t["category"]] += t["amount"]
        else:
            expense_by_cat[t["category"]] += t["amount"]

    total_income  = sum(income_by_cat.values())
    total_expense = sum(expense_by_cat.values())
    balance       = total_income - total_expense

    print(f"\n  Report for: {month_input}")
    print("  " + "-" * 40)

    if income_by_cat:
        print("\n  \033[92mINCOME\033[0m")
        for cat, amt in sorted(income_by_cat.items(), key=lambda x: -x[1]):
            print(f"    {cat:<25} {fmt_money(amt)}")
        print(f"    {'TOTAL':<25} {fmt_money(total_income)}")

    if expense_by_cat:
        print("\n  \033[91mEXPENSES\033[0m")
        for cat, amt in sorted(expense_by_cat.items(), key=lambda x: -x[1]):
            # Budget check
            budget = data["budgets"].get(cat)
            budget_note = ""
            if budget:
                pct = (amt / budget) * 100
                status = "✓" if amt <= budget else "⚠ OVER"
                budget_note = f"  (Budget: {fmt_money(budget)} | {pct:.0f}% {status})"
            print(f"    {cat:<25} {fmt_money(amt)}{budget_note}")
        print(f"    {'TOTAL':<25} {fmt_money(total_expense)}")

    print("\n  " + "-" * 40)
    bal_color = "\033[92m" if balance >= 0 else "\033[91m"
    print(f"  {bal_color}Net Balance: {fmt_money(balance)}\033[0m")
    input("\n  Press Enter to continue...")


def manage_budgets(data):
    header("Manage Budgets")

    expense_cats = CATEGORIES["expense"]
    budgets = data["budgets"]

    print("\n  Current budgets (monthly):\n")
    for cat in expense_cats:
        b = budgets.get(cat)
        status = fmt_money(b) if b else "Not set"
        print(f"    {cat:<25} {status}")

    print("\n  Options:")
    print("  1. Set/update a budget")
    print("  2. Remove a budget")
    print("  3. Back")
    choice = input("\n  Choose: ").strip()

    if choice == "1":
        for i, c in enumerate(expense_cats, 1):
            print(f"  {i}. {c}")
        try:
            idx = int(input("\n  Category number: ").strip()) - 1
            if not (0 <= idx < len(expense_cats)):
                raise ValueError
            cat = expense_cats[idx]
            amt = float(input(f"  Monthly budget for {cat} ($): ").strip())
            if amt <= 0:
                raise ValueError
            data["budgets"][cat] = round(amt, 2)
            save_data(data)
            print(f"\n  ✓ Budget set: {cat} → {fmt_money(amt)}/month")
        except (ValueError, IndexError):
            print("  Invalid input.")

    elif choice == "2":
        for i, c in enumerate(expense_cats, 1):
            print(f"  {i}. {c}")
        try:
            idx = int(input("\n  Category number to remove: ").strip()) - 1
            cat = expense_cats[idx]
            if cat in data["budgets"]:
                del data["budgets"][cat]
                save_data(data)
                print(f"\n  ✓ Budget removed for {cat}.")
            else:
                print("  No budget set for that category.")
        except (ValueError, IndexError):
            print("  Invalid input.")

    input("\n  Press Enter to continue...")


def summary_dashboard(data):
    header("Dashboard Summary")

    txns = data["transactions"]
    if not txns:
        print("\n  No transactions yet.")
        input("\n  Press Enter to continue...")
        return

    now = datetime.today()
    this_month = now.strftime("%Y-%m")

    all_income   = sum(t["amount"] for t in txns if t["type"] == "income")
    all_expense  = sum(t["amount"] for t in txns if t["type"] == "expense")
    all_balance  = all_income - all_expense

    mo_txns      = [t for t in txns if t["date"].startswith(this_month)]
    mo_income    = sum(t["amount"] for t in mo_txns if t["type"] == "income")
    mo_expense   = sum(t["amount"] for t in mo_txns if t["type"] == "expense")
    mo_balance   = mo_income - mo_expense

    print(f"\n  {'ALL TIME':}")
    print(f"    Income  : \033[92m{fmt_money(all_income)}\033[0m")
    print(f"    Expenses: \033[91m{fmt_money(all_expense)}\033[0m")
    bal_color = "\033[92m" if all_balance >= 0 else "\033[91m"
    print(f"    Balance : {bal_color}{fmt_money(all_balance)}\033[0m")

    print(f"\n  THIS MONTH ({this_month}):")
    print(f"    Income  : \033[92m{fmt_money(mo_income)}\033[0m")
    print(f"    Expenses: \033[91m{fmt_money(mo_expense)}\033[0m")
    bal_color = "\033[92m" if mo_balance >= 0 else "\033[91m"
    print(f"    Balance : {bal_color}{fmt_money(mo_balance)}\033[0m")

    if mo_txns:
        cat_totals = defaultdict(float)
        for t in mo_txns:
            if t["type"] == "expense":
                cat_totals[t["category"]] += t["amount"]
        if cat_totals:
            print("\n  TOP EXPENSE CATEGORIES THIS MONTH:")
            for cat, amt in sorted(cat_totals.items(), key=lambda x: -x[1])[:3]:
                bar_len = int((amt / mo_expense) * 20) if mo_expense else 0
                bar = "█" * bar_len
                print(f"    {cat:<20} {fmt_money(amt):>10}  {bar}")

    # Budget alerts
    if data["budgets"] and mo_txns:
        alerts = []
        for cat, budget in data["budgets"].items():
            spent = sum(t["amount"] for t in mo_txns if t["type"] == "expense" and t["category"] == cat)
            if spent > budget:
                alerts.append((cat, spent, budget))
        if alerts:
            print("\n  ⚠  BUDGET ALERTS:")
            for cat, spent, budget in alerts:
                print(f"    {cat}: spent {fmt_money(spent)} / budget {fmt_money(budget)}")

    print(f"\n  Total transactions: {len(txns)}")
    input("\n  Press Enter to continue...")



def main():
    data = load_data()

    while True:
        clear()
        print("\n\033[1m   Personal Finance Tracker\033[0m")
        print("  " + "─" * 35)
        print("  1.  Dashboard")
        print("  2.  Add Transaction")
        print("  3.  View All Transactions")
        print("  4.  Delete Transaction")
        print("  5.  Monthly Report")
        print("  6.  Manage Budgets")
        print("  7.  Exit")
        print()

        choice = input("  Choose an option (1-7): ").strip()

        if choice == "1":
            summary_dashboard(data)
        elif choice == "2":
            add_transaction(data)
        elif choice == "3":
            view_transactions(data)
        elif choice == "4":
            delete_transaction(data)
        elif choice == "5":
            monthly_report(data)
        elif choice == "6":
            manage_budgets(data)
        elif choice == "7":
            print("\n  Goodbye! 👋\n")
            break
        else:
            print("  Invalid choice. Try again.")
            input("  Press Enter to continue...")


if __name__ == "__main__":
    main()