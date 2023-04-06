from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate

from db import db
from resources.shops import blp as ShopBlueprint
from resources.products import blp as ProductBlueprint
from resources.tags import blp as TagBlueprint
import models


def create_app():
    app = Flask(__name__)

    app.config["API_TITLE"] = "Comparison toy"
    app.config["API_VERSION"] = "v. 1.0"

    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_VERSION"] = "3.1.0"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["OPENAPI_SWAGGER_UI_CONFIG"] = {"filter": True}

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SQLALCHEMY_ECHO'] = True

    db.init_app(app)
    migrate = Migrate(app, db)

    if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
        def _fk_pragma_on_connect(dbapi_con, con_record):  # noqa
            dbapi_con.execute('pragma foreign_keys=ON')

        with app.app_context():
            from sqlalchemy import event
            event.listen(db.engine, 'connect', _fk_pragma_on_connect)

    api = Api(app)

    api.register_blueprint(ShopBlueprint)
    api.register_blueprint(ProductBlueprint)
    api.register_blueprint(TagBlueprint)

    return app
