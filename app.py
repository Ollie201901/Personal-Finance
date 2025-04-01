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
    transactions = db.Transaction().get_all()
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

@app.route("/auto_categorization", methods = ["GET", "POST"])
def auto_categorization():
    return render_template("auto_categorization.html")

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
    return render_template("budget.html", categories = [])


if __name__ == "__main__":
    db.Database().create()
    app.run(host = "127.0.0.1", port = 2000, debug = True)
