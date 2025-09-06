from extensions import *

auth_bp = Blueprint("auth", __name__, template_folder=my_template)

# Sign Up
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for("auth.signup"))

        if User.query.filter_by(email=email).first():
            flash("Email already registered!", "error")
            return redirect(url_for("auth.signup"))

        new_user = User(full_name=full_name, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("signup.html")


# Login
@auth_bp.route("/", methods=["GET", "POST"])
# @auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            session["full_name"] = user.full_name
            flash("Login successful!", "success")
            return redirect(url_for("dashboard.dashboard"))

        flash("Invalid credentials", "error")
        return redirect(url_for("auth.login"))

    return render_template("login.html")


# Logout
@auth_bp.route("/logout", methods=['POST'])
def logout():
    session.clear()
    flash("Logged out successfully!", "info")
    return redirect(url_for("auth.login"))
