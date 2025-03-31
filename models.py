from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime

db = SQLAlchemy()

class TransactionType(db.Model):
    __tablename__ = "transaction_types"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    create_date = db.Column(db.String, nullable=False, server_default = func.now())
    delete_date = db.Column(db.String, nullable=True)

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    create_date = db.Column(db.String, nullable=False, server_default = func.now())
    delete_date = db.Column(db.String, nullable=True)
class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable = False)
    amount = db.Column(db.Float, nullable=False)
    transaction_type_id = db.Column(db.Integer, db.ForeignKey("transaction_types.id"), nullable = False) #Income, Expenses, Savings, Investments
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable = False)
    create_date = db.Column(db.String, nullable=False, server_default = func.now())
    delete_date = db.Column(db.String, nullable=True)

class TransactionSource(db.Model):
    __tablename__ = "transaction_source"
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    account_type = db.Column(db.String, nullable=False)
    create_date = db.Column(db.String, nullable=True, server_default = func.now())
    delete_date = db.Column(db.String, nullable=True)