from db import db


class TagsProducts(db.Model):
    __tablename__ = "tags_products"

    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey("tags.id", onupdate="CASCADE", ondelete="RESTRICT"),
                       unique=False,
                       nullable=False)
    product_id = db.Column(db.Integer,
                           db.ForeignKey("products.id", onupdate="CASCADE", ondelete="RESTRICT"),
                           unique=False,
                           nullable=False)
