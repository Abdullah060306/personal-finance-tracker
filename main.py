from tracker import initialize_data_file, add_transaction, get_all_transactions, delete_transaction, CATEGORIES
from reports import monthly_summary, category_breakdown, check_budget_alerts
from charts import show_charts


def show_menu():
    print("\n" + "=" * 40)
    print("   💰 PERSONAL FINANCE TRACKER")
    print("=" * 40)
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View All Transactions")
    print("4. Delete a Transaction")
    print("5. Monthly Summary")
    print("6. Category Breakdown")
    print("7. Show Charts")
    print("8. Budget Alerts")
    print("9. Exit")
    print("=" * 40)


def get_amount():
    while True:
        try:
            amount = float(input("Enter amount (₹): "))
            if amount <= 0:
                print("Amount must be greater than 0.")
                continue
            return amount
        except ValueError:
            print("Please enter a valid number.")


def choose_category(trans_type):
    print(f"\nAvailable {trans_type} categories:")
    cats = CATEGORIES[trans_type]
    for i, cat in enumerate(cats, 1):
        print(f"  {i}. {cat}")
    
    while True:
        try:
            choice = int(input(f"Choose category (1-{len(cats)}): "))
            if 1 <= choice <= len(cats):
                return cats[choice - 1]
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a number.")


def add_new_transaction(trans_type):
    print(f"\n--- Add New {trans_type.title()} ---")
    amount = get_amount()
    category = choose_category(trans_type)
    description = input("Enter description: ").strip()
    
    add_transaction(amount, category, description, trans_type)


def view_transactions():
    transactions = get_all_transactions()
    
    if not transactions:
        print("\n📭 No transactions found.")
        return
    
    print("\n" + "-" * 70)
    print(f"{'#':<4} {'Date':<12} {'Type':<10} {'Amount':<10} {'Category':<12} {'Description'}")
    print("-" * 70)
    
    for i, t in enumerate(transactions):
        sign = "+" if t["type"] == "income" else "-"
        print(f"{i:<4} {t['date']:<12} {t['type']:<10} {sign}₹{t['amount']:<9} {t['category']:<12} {t['description']}")
    
    print("-" * 70)


def delete_menu():
    view_transactions()
    transactions = get_all_transactions()
    
    if not transactions:
        return
    
    try:
        index = int(input("\nEnter the number (#) of transaction to delete: "))
        delete_transaction(index)
    except ValueError:
        print("Please enter a valid number.")


def main():
    initialize_data_file()
    
    while True:
        show_menu()
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == "1":
            add_new_transaction("income")
        elif choice == "2":
            add_new_transaction("expense")
        elif choice == "3":
            view_transactions()
        elif choice == "4":
            delete_menu()
        elif choice == "5":
            monthly_summary()
        elif choice == "6":
            category_breakdown()
        elif choice == "7":
            show_charts()
        elif choice == "8":
            check_budget_alerts()
        elif choice == "9":
            print("\n👋 Goodbye! Your data is saved.")
            break
        else:
            print("\n❌ Invalid choice. Please enter 1-9.")


if __name__ == "__main__":
    main()