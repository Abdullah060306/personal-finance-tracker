from flask import Flask, render_template, request, redirect, url_for
from tracker import initialize_data_file, add_transaction, get_all_transactions, delete_transaction, CATEGORIES
from reports import monthly_summary_data, category_breakdown_data
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def home():
    transactions = get_all_transactions()
    total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    total_expense = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    savings = total_income - total_expense
    
    return render_template('index.html', 
                         transactions=transactions,
                         total_income=total_income,
                         total_expense=total_expense,
                         savings=savings,
                         count=len(transactions))

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        trans_type = request.form['type']
        amount = float(request.form['amount'])
        category = request.form['category']
        description = request.form['description']
        
        add_transaction(amount, category, description, trans_type)
        return redirect(url_for('home'))
    
    return render_template('add.html', categories=CATEGORIES)

@app.route('/delete/<int:index>')
def delete(index):
    delete_transaction(index)
    return redirect(url_for('home'))

@app.route('/reports')
def reports():
    transactions = get_all_transactions()
    
    # Monthly data
    current_month = datetime.now().strftime("%Y-%m")
    month_data = monthly_summary_data(current_month)
    
    # Category data
    cat_data = category_breakdown_data(current_month)
    
    return render_template('reports.html', 
                         month_data=month_data,
                         cat_data=cat_data,
                         current_month=current_month)
    if __name__ == '__main__':
        initialize_data_file()
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    if __name__ == '__main__':
        initialize_data_file()
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)