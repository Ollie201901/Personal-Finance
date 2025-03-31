from flask import Flask, render_template, request, redirect, jsonify
from models import db, Transaction, TransactionType, Category, TransactionSource
from Transaction import Transaction
import utils


app = Flask(__name__)

# Configure the SQLite database URI and disable modification tracking
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Create the database tables if they don't exist
with app.app_context():
    db.create_all()

# Defining Routes
@app.route("/", methods = ["GET", "POST"])
def index():
    return redirect("/transactions")
    # return redirect("/dashboard")

@app.route("/dashboard", methods = ["GET", "POST"])
def dashboard():
    return render_template("dashboard.html")


@app.route("/transactions", methods = ["GET", "POST"])
def transactions():
    return render_template("transactions.html",transactions = [])

@app.route("/scheduled_transactions", methods = ["GET", "POST"])
def scheduled_transactions():
    return render_template("scheduled_transactions.html")

@app.route("/predicted_transactions", methods = ["GET", "POST"])
def predicted_transactions():
    return render_template("predicted_transactions.html")

@app.route("/auto_categorization", methods = ["GET", "POST"])
def auto_categorization():
    return render_template("auto_categorization.html")

@app.route("/transaction_settings", methods = ["GET", "POST"])
def transaction_settings():
    transaction_source = TransactionSource.query.all()
    return render_template("transaction_settings.html", transaction_source = transaction_source)

@app.route("/transaction_settings_form_submit", methods = ["GET", "POST"])
def transaction_settings_form_submit():
    file_path = request.form.get("file_path")
    file_name = request.form.get("file_name")
    account_type = request.form.get("account_type")
    transaction_source = TransactionSource(path=file_path,name=file_name,account_type=account_type)
    db.session.add(transaction_source)
    db.session.commit()
    return redirect("/transaction_settings")
@app.route("/budget", methods = ["GET", "POST"])
def budget():
    return render_template("budget.html", categories = [])



@app.route('/bulk_import', methods=["GET", "POST"])
def bulk_import():
    # Check if a file was uploaded; if not, assume JSON data was sent (CSV parsed client-side)
    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected.'}), 400

        file_name = file.filename.lower()
        try:
            if file_name.endswith('.csv'):
                # Process CSV file uploaded via FormData
                new_transactions = utils.process_CSV(file,file_name)
            elif file_name.endswith('.xlsx'):
                # Process Excel file
                new_transactions = utils.process_xls(file,file_name)
            else:
                return jsonify({'success': False, 'error': 'Unsupported file type.'}), 400
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    else:
        # No file uploaded
        return jsonify({'success': False, 'error': 'No data provided.'}), 400


    try:
        # Get database transactions
        existing_transactions = utils.get_all_db_transactions()

        # Compare New with Existing
        result = utils.compare(new_transactions, existing_transactions)
        # Submit New Transactions
        !!!!
        return jsonify({'success': True, 'inserted': inserted_count})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host = "127.0.0.1", port = 2000, debug = True)
