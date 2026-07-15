import csv
import os
from datetime import datetime

DATA_FILE = os.path.join("data", "transactions.csv")

CATEGORIES = {
    "income": ["Salary", "Freelance", "Investment", "Gift", "Other Income"],
    "expense": ["Food", "Transport", "Shopping", "Entertainment", "Bills", "Health", "Education", "Other"]
}


def initialize_data_file():
    if not os.path.exists("data"):
        os.makedirs("data")
    
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "amount", "category", "description", "type"])


def add_transaction(amount, category, description, trans_type):
    date = datetime.now().strftime("%Y-%m-%d")
    
    with open(DATA_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, amount, category, description, trans_type])
    
    print(f"\n✅ Saved: {trans_type} of ₹{amount} for {category}")


def get_all_transactions():
    transactions = []
    
    with open(DATA_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            transactions.append({
                "date": row["date"],
                "amount": float(row["amount"]),
                "category": row["category"],
                "description": row["description"],
                "type": row["type"]
            })
    
    return transactions


def delete_transaction(index):
    transactions = get_all_transactions()
    
    if 0 <= index < len(transactions):
        removed = transactions.pop(index)
        
        with open(DATA_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "amount", "category", "description", "type"])
            for t in transactions:
                writer.writerow([t["date"], t["amount"], t["category"], t["description"], t["type"]])
        
        print(f"\n✅ Deleted: {removed['description']} (₹{removed['amount']})")
    else:
        print("\n❌ Invalid number. Please try again.")