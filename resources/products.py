from flask_smorest import Blueprint
from flask.views import MethodView

from models import ProductModel, ShopModel
from schema import PlainProductSchema, ProductSchemaListOutput, ProductSchemaIdOutput
from db import db

blp = Blueprint("products", __name__, description="Operations on products")


@blp.route("/products")
class ProductList(MethodView):

    @blp.response(200, ProductSchemaListOutput(many=True),
                  description="Returns all products.")
    def get(self):
        return ProductModel.query.all()


@blp.route("/products/<int:productId>")
class Product(MethodView):

    @blp.response(200, ProductSchemaIdOutput)
    def get(self, productId):
        product = db.get_or_404(ProductModel, productId)
        return product


@blp.route("/shop/<int:shopId>/products")
class ProductsInShop(MethodView):

    @blp.response(200, ProductSchemaListOutput(many=True),
                  description="Get all products from chosen shop.")
    def get(self, shopId):
        shop = db.get_or_404(ShopModel, shopId)
        return shop.products.all()

    @blp.arguments(PlainProductSchema,
                   description="Add product to chosen shop.")
    @blp.response(200, ProductSchemaIdOutput)
    def post(self, productData, shopId):
        shop = db.get_or_404(ShopModel, shopId)
        product = ProductModel(**productData, shop_id=shop.id)
        db.session.add(product)
        db.session.commit()
        return product
