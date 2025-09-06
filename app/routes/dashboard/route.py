from extensions import *
from datetime import datetime

dashboard_bp = Blueprint("dashboard", __name__, template_folder=my_template)


@dashboard_bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        flash("Please login first.", "error")
        return redirect(url_for("auth.login"))

    user = User.query.get(session["user_id"])
    if not user:
        flash("User not found.", "error")
        return redirect(url_for("auth.login"))

    return render_template(
        "dashboard.html",
        user=user
    )

