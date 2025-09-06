from extensions import *

transaction_api = Blueprint("transaction_api", __name__, url_prefix="/api/transaction")


# ---------------- READ ----------------
@transaction_api.route("/", methods=["GET"])
def get_transaction():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.get(session["user_id"])
    if not user:
        return jsonify({"error": "User not found"}), 404

    # --- Date Range filter ---
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    query = Transaction.query.filter_by(user_id=user.id)

    if start_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            query = query.filter(Transaction.date >= start_date)
        except Exception:
            return jsonify({"error": "Invalid start_date format. Use YYYY-MM-DD"}), 400

    if end_date:
        try:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            query = query.filter(Transaction.date <= end_date)
        except Exception:
            return jsonify({"error": "Invalid end_date format. Use YYYY-MM-DD"}), 400

    transactions = query.all()

    # Format transactions
    all_transactions = [
        {
            "id": t.id,
            "type": t.type,
            "category": t.category,
            "amount": float(t.amount),
            "date": t.date.strftime("%Y-%m-%d"),
            "notes": t.notes,
        }
        for t in transactions
    ]

    # --- 12-Month aggregation (apply same filters) ---
    monthly_query = db.session.query(
        extract("month", Transaction.date).label("month"),
        Transaction.type,
        func.sum(Transaction.amount).label("total")
    ).filter(Transaction.user_id == user.id)

    if start_date:
        monthly_query = monthly_query.filter(Transaction.date >= start_date)
    if end_date:
        monthly_query = monthly_query.filter(Transaction.date <= end_date)

    monthly_query = monthly_query.group_by("month", Transaction.type).all()

    monthly_income = [0] * 12
    monthly_expenses = [0] * 12
    for m, ttype, total in monthly_query:
        if ttype == "income":
            monthly_income[int(m) - 1] = float(total)
        elif ttype == "expense":
            monthly_expenses[int(m) - 1] = float(total)

    total_income = sum(monthly_income)
    total_expenses = sum(monthly_expenses)
    total_balance = total_income - total_expenses

    # --- Category breakdown (also filtered already) ---
    category_data = db.session.query(
        Transaction.category,
        func.sum(Transaction.amount).label("total")
    ).filter(Transaction.user_id == user.id, Transaction.type == "expense")

    if start_date:
        category_data = category_data.filter(Transaction.date >= start_date)
    if end_date:
        category_data = category_data.filter(Transaction.date <= end_date)

    category_data = category_data.group_by(Transaction.category).all()

    category_labels = [(row[0].capitalize() if row[0] else "Uncategorized") for row in category_data]
    category_totals = [float(row[1]) for row in category_data]

    return jsonify({
        "transactions": all_transactions,
        "monthly_income": monthly_income,
        "monthly_expenses": monthly_expenses,
        "category_labels": category_labels,
        "category_totals": category_totals,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "total_balance": total_balance
    })


# ---------------- GET SINGLE TRANSACTION ----------------
@transaction_api.route("/<int:transaction_id>", methods=["GET"])
def get_single_transaction(transaction_id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.user_id != session["user_id"]:
        return jsonify({"error": "Unauthorized"}), 403

    return jsonify({
        "id": transaction.id,
        "type": transaction.type,
        "category": transaction.category,
        "amount": float(transaction.amount),
        "date": transaction.date.strftime("%Y-%m-%d"),
        "notes": transaction.notes,
    })







# ---------------- CREATE ----------------
@transaction_api.route("/", methods=["POST"])
def create_transaction():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    try:
        transaction = Transaction(
            type=data["type"],
            category=data["category"],
            amount=float(data["amount"]),
            date=datetime.strptime(data["date"], "%Y-%m-%d").date(),
            notes=data.get("notes"),
            user_id=session["user_id"]
        )
        db.session.add(transaction)
        db.session.commit()
        return jsonify({"message": "Transaction created", "transaction_id": transaction.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# ---------------- UPDATE ----------------
@transaction_api.route("/<int:transaction_id>", methods=["PUT"])
def update_transaction(transaction_id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.user_id != session["user_id"]:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    try:
        transaction.type = data.get("type", transaction.type)
        transaction.category = data.get("category", transaction.category)
        transaction.amount = float(data.get("amount", transaction.amount))
        if "date" in data:
            transaction.date = datetime.strptime(data["date"], "%Y-%m-%d").date()
        transaction.notes = data.get("notes", transaction.notes)
        db.session.commit()
        return jsonify({"message": "Transaction updated", "transaction_id": transaction.id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# ---------------- DELETE ----------------
@transaction_api.route("/<int:transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.user_id != session["user_id"]:
        return jsonify({"error": "Unauthorized"}), 403

    try:
        db.session.delete(transaction)
        db.session.commit()
        return jsonify({"message": "Transaction deleted", "transaction_id": transaction.id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
