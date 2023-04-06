from datetime import datetime

from db import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)
    datetime_create = db.Column(db.DateTime(), default=datetime.now)
    datetime_update = db.Column(db.DateTime(), onupdate=datetime.now)
    shop_id = db.Column(db.Integer,
                        db.ForeignKey("shops.id"),
                        unique=False,
                        nullable=False)

    shop = db.relationship("ShopModel", back_populates="tags")
    products = db.relationship("ProductModel", back_populates="tags", secondary="tags_products")
