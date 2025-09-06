from extensions import *

transaction_bp = Blueprint("transaction", __name__, template_folder=my_template)


@transaction_bp.route("/transaction", methods=["GET", "POST"])
def transaction():
    if "user_id" not in session:
        flash("Please login first.", "error")
        return redirect(url_for("auth.login"))

    user = User.query.get(session["user_id"])
    if not user:
        flash("User not found.", "error")
        return redirect(url_for("auth.login"))

    return render_template(
        "transaction.html",
        user=user
    )

