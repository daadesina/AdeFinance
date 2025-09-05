from extensions import *

dashboard_bp = Blueprint("dashboard", __name__, template_folder=my_template)

# Dashboard (protected)
@dashboard_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please login first.", "error")
        return redirect(url_for("auth.login"))
    return render_template(
        "dashboard.html"
    )