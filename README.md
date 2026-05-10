#  Personal Finance Tracker

A lightweight, command-line personal finance tracker built in pure Python — no external libraries required. Track income and expenses, set monthly budgets, and view reports — all from your terminal.

---

##  Features

- **Dashboard** — at-a-glance summary of all-time and current month finances, top spending categories, and budget alerts
- **Add Transactions** — log income or expenses with category, description, amount, and date
- **View Transactions** — full transaction history sorted by date with color-coded amounts
- **Delete Transactions** — remove any entry by ID with a confirmation prompt
- **Monthly Reports** — detailed category breakdown for any month with budget vs. actual comparison
- **Budget Management** — set monthly spending limits per category and get notified when exceeded
- **Auto-save** — data is persisted automatically to `finance_data.json`

---

##  Getting Started

### Requirements

- Python 3.7 or higher
- No external packages needed

### Installation

1. Download or clone the file:

```bash
git clone https://github.com/Biniam-Girma-cyber/personal_finance.git
cd personal_finance
```

Or simply save `personal_finance.py` to a folder of your choice.

2.Run the program:

```bash
python personal_finance.py
```

---

##  Project Structure

```
finance-tracker/
├── finance_tracker.py   # Main application
├── finance_data.json    # Auto-generated data file (created on first run)
└── README.md
```

---

##  How to Use

### Main Menu

```
 Personal Finance Tracker
───────────────────────────────────
  1.   Dashboard
  2.   Add Transaction
  3.   View All Transactions
  4.   Delete Transaction
  5.   Monthly Report
  6.   Manage Budgets
  7.   Exit
```

### Adding a Transaction

1. Select option `2` from the main menu
2. Choose type: **Income** or **Expense**
3. Pick a category from the list
4. Enter a description, amount, and date (or press Enter for today)

### Income Categories
| Category       | Description                  |
|---------------|------------------------------|
| Salary         | Regular employment income    |
| Freelance      | Contract or gig work         |
| Investment     | Dividends, returns, etc.     |
| Gift           | Money received as a gift     |
| Other Income   | Any other income source      |

### Expense Categories
| Category        | Description                  |
|----------------|------------------------------|
| Food            | Groceries, restaurants       |
| Transport       | Fuel, bus, taxi, flights     |
| Housing         | Rent, utilities, repairs     |
| Health          | Medical, pharmacy, gym       |
| Entertainment   | Movies, games, subscriptions |
| Shopping        | Clothing, electronics, etc.  |
| Education       | Courses, books, tuition      |
| Other Expense   | Miscellaneous expenses       |

### Setting Budgets

1. Select option `6` — Manage Budgets
2. Choose **Set/update a budget**
3. Pick an expense category and enter a monthly limit

Budget warnings appear in the **Dashboard** and **Monthly Report** whenever spending exceeds the limit for that category.

### Monthly Report

1. Select option `5` — Monthly Report
2. Enter a month in `YYYY-MM` format (e.g. `2026-05`), or press Enter for the current month
3. View income and expenses broken down by category, with budget comparison where applicable

---

##  Data Storage

All data is saved to `finance_data.json` in the same directory as the script. The file is created automatically on first run.

Example structure:

```json
{
  "transactions": [
    {
      "id": 1,
      "type": "income",
      "category": "Salary",
      "description": "Monthly salary",
      "amount": 3000.00,
      "date": "2026-05-01"
    }
  ],
  "budgets": {
    "Food": 300.00,
    "Transport": 100.00
  }
}
```

You can back up this file at any time to preserve your data.

---

##  Example Output

```
  ALL TIME:
    Income  : $5,200.00
    Expenses: $1,860.00
    Balance : $3,340.00

  THIS MONTH (2026-05):
    Income  : $3,000.00
    Expenses: $560.00
    Balance : $2,440.00

  TOP EXPENSE CATEGORIES THIS MONTH:
    Housing              $300.00   ████████████
    Food                 $160.00   ██████
    Transport             $100.00  ████

  ⚠  BUDGET ALERTS:
    Food: spent $160.00 / budget $150.00
```

---

##  Customization

To add your own categories, edit the `CATEGORIES` dictionary near the top of `finance_tracker.py`:

```python
CATEGORIES = {
    "income":  ["Salary", "Freelance", "Investment", "Gift", "Other Income"],
    "expense": ["Food", "Transport", "Housing", "Health", "Entertainment",
                "Shopping", "Education", "Other Expense"],
}
```

---

## License

MIT License — free to use, modify, and distribute.
