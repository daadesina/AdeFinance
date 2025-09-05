from extensions import *

base_bp = Blueprint("base", __name__, template_folder=my_template)

@base_bp.route("/base")
def base():
    return render_template(
        "base.html"
    )