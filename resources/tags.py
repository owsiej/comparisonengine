from flask_smorest import Blueprint
from flask.views import MethodView

blp = Blueprint("tags", __name__, description="Operations on tags")


@blp.route("/products")
class TagList(MethodView):
    def get(self):
        pass

    def post(self):
        pass
