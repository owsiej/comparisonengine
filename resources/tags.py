from flask_smorest import Blueprint, abort
from flask.views import MethodView

from db import db
from models import TagModel, ShopModel, ProductModel
from schema import PlainTagSchema, TagSchemaListOutput, TagSchemaIdOutPut, TagsProducts

blp = Blueprint("tags", __name__, description="Operations on tags")


@blp.route("/tags")
class TagList(MethodView):
    @blp.response(200, TagSchemaListOutput, description="Returns all tags.")
    def get(self):
        return TagModel.query.all()


@blp.route("/shop/<int:shopId>/tags")
class TagInShop(MethodView):
    @blp.response(200, TagSchemaListOutput, description="Returns tags in requested shop.")
    @blp.alt_response(404, description="Occurs when shop with requested id doesn't exist.")
    def get(self, shopId):
        shop = db.get_or_404(ShopModel, shopId)
        return shop.tags.all()

    @blp.arguments(PlainTagSchema, description="Pass data of a new tag.")
    @blp.response(200, TagSchemaIdOutPut, description="Adds tag to requested shop.")
    @blp.alt_response(404, description="Occurs when shop with requested id doesn't exist.")
    def post(self, tagData, shopId):
        shop = db.get_or_404(ShopModel, shopId)
        if shop.tags.filter_by(name=tagData['name']).first():
            abort(400, message="Tag with requested name already exist in shop.")
        tag = TagModel(**tagData, shop_id=shopId)
        db.session.add(tag)
        db.session.commit()
        return tag

    @blp.response(200, description="Deletes all tags from shop.")
    def delete(self, shopId):
        shop = db.get_or_404(ShopModel, shopId)
        db.session.delete(*shop.tags.all())
        db.session.commit()
        return {"message": "All tags from shop successfully deleted."}


@blp.route("/tag/<int:tagId>")
class Tag(MethodView):
    @blp.response(200, TagSchemaIdOutPut, description="Returns requested tag.")
    @blp.alt_response(404, description="Occurs when tag with requested id doesn't exist.")
    def get(self, tagId):
        tag = db.get_or_404(TagModel, tagId)
        return tag

    @blp.arguments(PlainTagSchema, description="Pass data to update requested tag.")
    @blp.response(200, TagSchemaIdOutPut, description="Updates requested tag.")
    @blp.alt_response(404, description="Occurs when tag with requested id doesn't exist.")
    def put(self, tagData, tagId):
        tag = db.get_or_404(TagModel, tagId)
        shop = db.get_or_404(ShopModel, tag.shop_id)
        if shop.tags.filter_by(name=tagData['name']).first():
            abort(400, message="Tag with requested name already exist in shop.")
        tag.name = tagData['name']
        db.session.add(tag)
        db.session.commit()
        return tag

    @blp.response(200, description="Delete requested tag.")
    @blp.alt_response(404, description="Occurs when tag with requested id doesn't exist.")
    def delete(self, tagId):
        tag = db.get_or_404(TagModel, tagId)
        db.session.delete(tag)
        db.session.commit()
        return {"message": "Tag deleted successfully."}


@blp.route("/products/<int:productId>/tags/<int:tagId>")
class LinkTagToProduct(MethodView):
    @blp.response(200, TagSchemaIdOutPut)
    @blp.alt_response(404, description="Occurs when tag or product with requested id doesn't exist.")
    def post(self, productId, tagId):
        product = db.get_or_404(ProductModel, productId)
        tag = db.get_or_404(TagModel, tagId)
        product.tags.append(tag)
        db.session.add(product)
        db.session.commit()
        return tag

    @blp.response(200, TagsProducts)
    def delete(self, productId, tagId):
        product = db.get_or_404(ProductModel, productId)
        tag = db.get_or_404(TagModel, tagId)
        product.tags.remove(tag)
        db.session.add(product)
        db.session.commit()
        return {"message": "Tag successfully unlinked from product",
                "tag": tag,
                "product": product}
