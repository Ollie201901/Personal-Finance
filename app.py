from flask import Flask, render_template, request, redirect, jsonify
import database as db

import utils

app = Flask(__name__)
# Defining Routes
@app.route("/", methods = ["GET", "POST"])
def index():
    return redirect("/transactions")

@app.route("/transactions", methods = ["GET", "POST"])
def transactions():
    with db.Transaction() as t:
        transactions = t.get_all()
    return render_template("transactions.html",transactions = transactions)
@app.route('/bulk_import', methods=["GET", "POST"])
def bulk_import():
    utils.bulk_import()
    return redirect("/transactions")
    # Check if a file was uploaded; if not, assume JSON data was sent (CSV parsed client-side)
    # if 'file' in request.files:
    #     file = request.files['file']
    #     if file.filename == '':
    #         return jsonify({'success': False, 'error': 'No file selected.'}), 400
    #
    #     file_name = file.filename.lower()
    #     try:
    #         if file_name.endswith('.csv'):
    #             # Process CSV file uploaded via FormData
    #             new_transactions = utils.process_CSV(file,file_name)
    #         elif file_name.endswith('.xlsx'):
    #             # Process Excel file
    #             new_transactions = utils.process_xls(file,file_name)
    #         else:
    #             return jsonify({'success': False, 'error': 'Unsupported file type.'}), 400
    #     except Exception as e:
    #         return jsonify({'success': False, 'error': str(e)}), 500
    # else:
    #     # No file uploaded
    #     return jsonify({'success': False, 'error': 'No data provided.'}), 400
    #
    #
    # try:
    #     # Get database transactions
    #     existing_transactions = utils.get_all_db_transactions()
    #
    #     # Compare New with Existing
    #     result = utils.compare(new_transactions, existing_transactions)
    #     # Submit New Transactions
    #     return jsonify({'success': True, 'inserted': inserted_count})
    # except Exception as e:
    #     return jsonify({'success': False, 'error': str(e)}), 500


@app.route("/scheduled_transactions", methods = ["GET", "POST"])
def scheduled_transactions():
    return render_template("scheduled_transactions.html",transaction_source = [])

@app.route("/predicted_transactions", methods = ["GET", "POST"])
def predicted_transactions():
    return render_template("predicted_transactions.html")


@app.route("/transaction_sources", methods = ["GET", "POST"])
def transaction_sources():
    with db.TransactionSource() as t:
        transaction_source = t.get_all()
    return render_template("transaction_sources.html", transaction_source = transaction_source)

@app.route("/transaction_sources_add", methods = ["GET", "POST"])
def transaction_sources_add():
    folder_path = request.form.get("folder_path")
    file_identifier = request.form.get("file_identifier")
    account_alias = request.form.get("account_alias")
    with db.TransactionSource() as t:
        t.add(folder_path=folder_path, file_identifier=file_identifier, account_alias=account_alias)
    return redirect("/transaction_sources")

@app.route("/categories_add", methods = ["GET", "POST"])
def categories_add():
    category = request.form.get("category")
    transaction_type = request.form.get("transaction_type")
    with db.Category() as c:
        c.add(category_name=category, transaction_type=transaction_type)
    return redirect("/categories")

@app.route('/transaction_sources/<int:transaction_source_id>/delete', methods=['POST'])
def delete_transaction_source(transaction_source_id):
    try:
        with db.TransactionSource() as t:
            t.delete(transaction_source_id)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    else: return jsonify({'success': True})


@app.route("/budget", methods = ["GET", "POST"])
def budget():
    with db.Budget() as b:
        budgets = b.get_all()
    with db.Category() as c:
        categories = c.get_all()
    return render_template("budget.html", budgets = budgets, categories= categories)

@app.route("/budget_add", methods = ["GET", "POST"])
def budget_add():
    category = request.form.get("category")
    threshold_amount = request.form.get("threshold_amount")
    period = request.form.get("frequency")
    match period.lower():
        case "weekly":
            period_days = 7
        case "bi-weekly":
            period_days = 14
        case "monthly":
            period_days = 31
        case "bi-monthly":
            period_days = 62
        case "6-months":
            period_days = 26*7
        case "yearly":
            period_days = 365
        case _:
            period_days = 1
    with db.Budget() as b:
        b.add(category=category,threshold_per_period=threshold_amount,period_days=period_days)
    return redirect("/budget")

@app.route('/budget/<int:budget_id>/delete', methods=['POST'])
def delete_budget(budget_id):
    try:
        with db.Budget() as b:
            b.delete(budget_id)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    else: return jsonify({'success': True})

@app.route("/categories", methods = ["GET", "POST"])
def categories():
    with db.Category() as c:
        categories = c.get_all()
    return render_template("categories.html", categories = categories)

@app.route('/category/<int:category_id>/delete', methods=['POST'])
def delete_category(category_id):
    try:
        with db.Category() as c:
            c.delete(category_id)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    else: return jsonify({'success': True})

if __name__ == "__main__":
    db.Database().create()
    app.run(host = "127.0.0.1", port = 2000, debug = True)
