from tracker import get_all_transactions
from collections import defaultdict
from datetime import datetime


def monthly_summary():
    """Show total income, expenses, and savings for a specific month."""
    transactions = get_all_transactions()
    
    if not transactions:
        print("\n📭 No transactions found.")
        return
    
    month = input("\nEnter month (YYYY-MM, e.g., 2026-07): ").strip()
    month_data = monthly_summary_data(month)
    
    print("\n" + "=" * 40)
    print(f"   📊 MONTHLY SUMMARY: {month}")
    print("=" * 40)
    print(f"   Total Income:   +₹{month_data['income']:,.2f}")
    print(f"   Total Expenses: -₹{month_data['expense']:,.2f}")
    print(f"   Net Savings:    ₹{month_data['savings']:,.2f}")
    print("=" * 40)
    
    if month_data['savings'] > 0:
        print("   🟢 You're saving money! Great job!")
    elif month_data['savings'] < 0:
        print("   🔴 You're spending more than you earn!")
    else:
        print("   ⚪ Break-even month.")
    print("=" * 40)


def monthly_summary_data(month):
    """Return monthly data as dictionary for web app."""
    transactions = get_all_transactions()
    
    total_income = 0
    total_expense = 0
    
    for t in transactions:
        if t["date"].startswith(month):
            if t["type"] == "income":
                total_income += t["amount"]
            else:
                total_expense += t["amount"]
    
    return {
        'income': total_income,
        'expense': total_expense,
        'savings': total_income - total_expense
    }


def category_breakdown():
    """Show how much spent in each category."""
    transactions = get_all_transactions()
    
    if not transactions:
        print("\n📭 No transactions found.")
        return
    
    month = input("\nEnter month (YYYY-MM, e.g., 2026-07): ").strip()
    cat_data = category_breakdown_data(month)
    
    if not cat_data:
        print(f"\n📭 No expenses found for {month}.")
        return
    
    print("\n" + "=" * 40)
    print(f"   📊 CATEGORY BREAKDOWN: {month}")
    print("=" * 40)
    
    total_spent = sum(item['amount'] for item in cat_data)
    
    for item in cat_data:
        percentage = (item['amount'] / total_spent) * 100
        bar = "█" * int(percentage / 5)
        print(f"   {item['category']:<12} ₹{item['amount']:>10,.2f} ({percentage:>5.1f}%) {bar}")
    
    print("=" * 40)
    print(f"   Total Spent:   ₹{total_spent:,.2f}")
    print("=" * 40)


def category_breakdown_data(month):
    """Return category data as list for web app."""
    transactions = get_all_transactions()
    
    category_totals = defaultdict(float)
    
    for t in transactions:
        if t["date"].startswith(month) and t["type"] == "expense":
            category_totals[t["category"]] += t["amount"]
    
    result = []
    for category, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
        result.append({
            'category': category,
            'amount': amount
        })
    
    return result


def check_budget_alerts():
    """Check if any category is over budget."""
    transactions = get_all_transactions()
    
    if not transactions:
        print("\n📭 No transactions found.")
        return
    
    budgets = {
        "Food": 5000,
        "Transport": 3000,
        "Shopping": 10000,
        "Entertainment": 2000,
        "Bills": 5000,
        "Health": 2000,
        "Education": 5000,
        "Other": 3000
    }
    
    current_month = datetime.now().strftime("%Y-%m")
    category_totals = defaultdict(float)
    
    for t in transactions:
        if t["date"].startswith(current_month) and t["type"] == "expense":
            category_totals[t["category"]] += t["amount"]
    
    print("\n" + "=" * 50)
    print("   🚨 BUDGET ALERTS")
    print("=" * 50)
    
    alerts_found = False
    
    for category, spent in category_totals.items():
        if category in budgets:
            limit = budgets[category]
            percentage = (spent / limit) * 100
            
            if spent > limit:
                print(f"   🔴 {category}: ₹{spent:,.2f} / ₹{limit:,.2f} ({percentage:.1f}%) - OVER BUDGET!")
                alerts_found = True
            elif percentage >= 80:
                print(f"   🟡 {category}: ₹{spent:,.2f} / ₹{limit:,.2f} ({percentage:.1f}%) - Warning!")
                alerts_found = True
    
    if not alerts_found:
        print("   🟢 All categories within budget! Great job!")
    
    print("=" * 50)