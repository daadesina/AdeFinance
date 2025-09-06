from database import db
from datetime import datetime

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)  # "income" or "expense"
    category = db.Column(db.String(50), nullable=True) #I just changed this to be nullable, I can I make it effective in the database witout deleteing the database 
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)

    # Link to User
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref="transactions")
