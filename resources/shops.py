from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from models import ShopModel
from schema import PlainShopSchema, ShopSchemaListOutput, ShopSchemaIdOutput
from db import db

blp = Blueprint("shops", __name__, description="Operations on shops")


@blp.route("/shops")
class ShopList(MethodView):

    @blp.response(200, ShopSchemaListOutput(many=True), description="Return list of all shops.")
    def get(self):
        return ShopModel.query.all()

    @blp.arguments(PlainShopSchema, description="Take args of new shop to add.")
    @blp.response(201, ShopSchemaIdOutput)
    @blp.alt_response(400, description="Occurs when passed shop already exists",
                      example={"message": "Shop with requested name already exists."})
    @blp.alt_response(422, description="Occurs when passed args are wrong data type or are missing",
                      example={"message": "Not a valid string.",
                               "message2": "Missing data for required field."})
    def post(self, shopData):
        shop = ShopModel(**shopData)
        try:
            db.session.add(shop)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Shop with requested name already exists.")
        return shop


@blp.route("/shops/<int:shopId>")
class Shop(MethodView):

    @blp.response(200, ShopSchemaIdOutput, description="Take shop id to return.")
    @blp.alt_response(404, description="Chosen shop doesn't exist.")
    def get(self, shopId):
        return db.get_or_404(ShopModel, shopId)

    @blp.arguments(PlainShopSchema)
    @blp.response(200, ShopSchemaIdOutput, description="Returns updated shop.")
    @blp.alt_response(404, description="Chosen shop doesn't exist.")
    @blp.alt_response(422, description="Occurs when passed args are wrong data type or are missing",
                      example={"message": "Not a valid string.",
                               "message2": "Missing data for required field."})
    def put(self, shopData, shopId):
        shop = db.get_or_404(ShopModel, shopId)
        shop.name = shopData['name']
        try:
            db.session.add(shop)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Shop with requested name already exists.")
        return shop

    @blp.response(200,
                  description="Deletes chosen shop",
                  example={
                      "message": "Shop deleted successfully."
                  })
    @blp.alt_response(404, description="Chosen shop doesn't exist.")
    def delete(self, shopId):
        shop = db.get_or_404(ShopModel, shopId)
        try:
            db.session.delete(shop)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Deleting shop with products in it is forbidden.")
        return {"message": "Shop deleted successfully."}
