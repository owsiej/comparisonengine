from flask_smorest import Blueprint
from flask.views import MethodView

from models import ShopModel
from schema import PlainShopSchema, ShopSchemaListOutput, ShopSchemaIdOutput
from db import db

blp = Blueprint("shops", __name__, description="Operations on shops")


@blp.route("/shops")
class ShopList(MethodView):

    @blp.response(200, ShopSchemaListOutput(many=True))
    def get(self):
        return ShopModel.query.all()

    @blp.arguments(PlainShopSchema)
    @blp.response(200, ShopSchemaIdOutput)
    def post(self, shopData):
        shop = ShopModel(**shopData)
        db.session.add(shop)
        db.session.commit()
        return shop


@blp.route("/shops/<int:shopId>")
class Shop(MethodView):

    @blp.response(200, ShopSchemaIdOutput)
    @blp.alt_response(404, description="Chosen shop doesn't exist.")
    def get(self, shopId):
        return db.get_or_404(ShopModel, shopId)

    @blp.arguments(PlainShopSchema)
    @blp.response(200, ShopSchemaIdOutput)
    @blp.alt_response(404, description="Chosen shop doesn't exist.")
    def put(self, shopData, shopId):
        shop = db.get_or_404(ShopModel, shopId)
        shop.name = shopData['name']
        db.session.add(shop)
        db.session.commit()
        return shop

    @blp.response(201,
                  description="Deletes chosen shop",
                  example={
                      "message": "Shop deleted successfully."
                  })
    @blp.alt_response(404, description="Chosen shop doesn't exist.")
    def delete(self, shopId):
        shop = db.get_or_404(ShopModel, shopId)
        db.session.delete(shop)
        db.session.commit()
        return {"message": "Shop deleted successfully."}
