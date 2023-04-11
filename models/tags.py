from datetime import datetime

from db import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=False, nullable=False)
    datetime_create = db.Column(db.DateTime(), default=datetime.now)
    datetime_update = db.Column(db.DateTime(), onupdate=datetime.now)
    shop_id = db.Column(db.Integer,
                        db.ForeignKey("shops.id", onupdate="CASCADE", ondelete="CASCADE"),
                        unique=False,
                        nullable=False)

    shop = db.relationship("ShopModel", back_populates="tags", passive_deletes=True)
    products = db.relationship("ProductModel", back_populates="tags", secondary="tags_products")
