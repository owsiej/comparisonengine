from datetime import datetime
from db import db


class ShopModel(db.Model):
    __tablename__ = "shops"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    datetime_create = db.Column(db.DateTime(), default=datetime.now)
    datetime_update = db.Column(db.DateTime(), onupdate=datetime.now)

    tags = db.relationship("TagModel", back_populates="shop", lazy="dynamic", cascade="all, delete")
    products = db.relationship("ProductModel", back_populates="shop", lazy="dynamic")
