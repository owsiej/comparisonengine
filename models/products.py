from datetime import datetime

from db import db


class ProductModel(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=False, nullable=False)
    price = db.Column(db.Float, nullable=False)
    datetime_create = db.Column(db.DateTime(), default=datetime.now)
    datetime_update = db.Column(db.DateTime(), onupdate=datetime.now)
    shop_id = db.Column(db.Integer,
                        db.ForeignKey("shops.id", onupdate="CASCADE", ondelete="RESTRICT"),
                        unique=False,
                        nullable=False)

    shop = db.relationship("ShopModel", back_populates="products")
    tags = db.relationship("TagModel", back_populates="products", secondary="tags_products")
