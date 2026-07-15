import matplotlib.pyplot as plt
from tracker import get_all_transactions
from collections import defaultdict


def show_charts():
    """Display visual charts for income vs expenses and category breakdown."""
    transactions = get_all_transactions()
    
    if not transactions:
        print("\n📭 No transactions found.")
        return
    
    month = input("\nEnter month (YYYY-MM, e.g., 2026-07): ").strip()
    
    # Filter transactions for the selected month
    month_transactions = [t for t in transactions if t["date"].startswith(month)]
    
    if not month_transactions:
        print(f"\n📭 No transactions found for {month}.")
        return
    
    # Calculate totals
    total_income = sum(t["amount"] for t in month_transactions if t["type"] == "income")
    total_expense = sum(t["amount"] for t in month_transactions if t["type"] == "expense")
    
    # Calculate category breakdown for expenses
    category_totals = defaultdict(float)
    for t in month_transactions:
        if t["type"] == "expense":
            category_totals[t["category"]] += t["amount"]
    
    # Create figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(f'Finance Dashboard - {month}', fontsize=16, fontweight='bold')
    
    # Chart 1: Income vs Expenses (Bar Chart)
    categories = ['Income', 'Expenses']
    values = [total_income, total_expense]
    colors = ['#2ecc71', '#e74c3c']
    
    bars = ax1.bar(categories, values, color=colors, edgecolor='black', linewidth=1.5)
    ax1.set_title('Income vs Expenses', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Amount (₹)', fontsize=12)
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'₹{value:,.0f}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Chart 2: Expense Breakdown (Pie Chart)
    if category_totals:
        labels = list(category_totals.keys())
        sizes = list(category_totals.values())
        colors_pie = plt.cm.Set3(range(len(labels)))
        
        wedges, texts, autotexts = ax2.pie(sizes, labels=labels, autopct='%1.1f%%',
                                            colors=colors_pie, startangle=90,
                                            textprops={'fontsize': 10})
        ax2.set_title('Expense Breakdown', fontsize=14, fontweight='bold')
        
        # Make percentage text bold
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)
    else:
        ax2.text(0.5, 0.5, 'No Expenses', ha='center', va='center', 
                fontsize=14, transform=ax2.transAxes)
        ax2.set_title('Expense Breakdown', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.show()
    
    print(f"\n📊 Charts displayed for {month}!")
    print(f"   Income: ₹{total_income:,.2f}")
    print(f"   Expenses: ₹{total_expense:,.2f}")
    print(f"   Savings: ₹{total_income - total_expense:,.2f}")