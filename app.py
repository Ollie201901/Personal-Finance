from flask import Flask, render_template, request, redirect, jsonify
from database import create_db, bulk_import_from_csv


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/", methods = ["GET", "POST"])
def index():
    return redirect("/dashboard")

@app.route("/dashboard", methods = ["GET", "POST"])
def dashboard():
    return  render_template("index.html")


@app.route("/transactions", methods = ["GET", "POST"])
def transactions():
    return render_template("transactions.html",transactions = [])

@app.route("/scheduled_transactions", methods = ["GET", "POST"])
def scheduled_transactions():
    return render_template("scheduled_transactions.html")

@app.route("/auto_categorization", methods = ["GET", "POST"])
def auto_categorization():
    return render_template("auto_categorization.html")

@app.route("/budget", methods = ["GET", "POST"])
def budget():
    return render_template("budget.html", categories = [])


# @app.route('/import_csv', methods=['POST'])
# def import_csv():
#     data = request.get_json().get('data')
#     if data:
#         try:
#             bulk_import_from_csv(data)
#             return jsonify({'success': True})
#         except Exception as e:
#             print(f'Error: {e}')
#             return jsonify({'success': False})
#     else:
#         return jsonify({'success': False})

if __name__ == "__main__":
    #create_db()
    app.run(host = "127.0.0.1",port=2000)
