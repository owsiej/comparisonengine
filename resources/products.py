from flask_smorest import Blueprint, abort
from flask.views import MethodView

from models import ProductModel, ShopModel
from schema import PlainProductSchema, ProductSchemaListOutput, ProductSchemaIdOutput, ProductSchemaUpdate
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
    @blp.alt_response(404, description="Chosen shop doesn't exist.")
    def get(self, productId):
        product = db.get_or_404(ProductModel, productId)
        return product

    @blp.arguments(ProductSchemaUpdate,
                   description="Pass new name and price of product.")
    @blp.response(200, ProductSchemaIdOutput,
                  description="Return updated product info.")
    @blp.alt_response(400, description="Occurs when shop with requested name already exists.",
                      example={"message": "Product with requested name is already in shop."})
    @blp.alt_response(422, description="Occurs when passed args are wrong data type or are missing",
                      example={"message": "Not a valid string.",
                               "message2": "Missing data for required field."})
    def put(self, productData, productId):
        product = db.get_or_404(ProductModel, productId)
        if productData.get("name"):
            shop = db.get_or_404(ShopModel, product.shop_id)
            if shop.products.filter_by(name=productData['name']).first():
                abort(400, message="Product with requested name is already in shop.")
            product.name = productData['name']
        product.price = productData['price'] if productData.get('price') else product.price
        db.session.add(product)
        db.session.commit()
        return product

    @blp.response(200, description="Delete chosen product")
    @blp.alt_response(404, description="Chosen product doesn't exist.")
    def delete(self, productId):
        product = db.get_or_404(ProductModel, productId)
        db.session.delete(product)
        db.session.commit()
        return {"message": "Product deleted successfully."}


@blp.route("/shops/<int:shopId>/products")
class ProductsInShop(MethodView):

    @blp.response(200, ProductSchemaListOutput(many=True),
                  description="Returns all products from chosen shop.")
    def get(self, shopId):
        shop = db.get_or_404(ShopModel, shopId)
        return shop.products.all()

    @blp.arguments(PlainProductSchema,
                   description="Add product to chosen shop.")
    @blp.response(201, ProductSchemaIdOutput, description="Product successfully added to shop.")
    @blp.alt_response(400, description="Occurs when requested new name of product already exist.",
                      example={"message": "Product with requested name is already in shop."})
    @blp.alt_response(404, description="Occurs when shop with given id doesn't exist.")
    @blp.alt_response(422, description="Occurs when passed args are wrong data type or are missing",
                      example={"message": "Not a valid string.",
                               "message2": "Missing data for required field."})
    def post(self, productData, shopId):
        shop = db.get_or_404(ShopModel, shopId)
        if shop.products.filter_by(name=productData['name']).first():
            abort(400, message="Product with requested name is already in shop.")
        product = ProductModel(**productData, shop_id=shop.id)
        db.session.add(product)
        db.session.commit()
        return product

    @blp.response(200, description="Delete all products from chosen shop")
    def delete(self, shopId):
        shop = db.get_or_404(ShopModel, shopId)
        db.session.delete(*shop.products.all())
        db.session.commit()
        return {"message": "All products from shop successfully deleted."}
