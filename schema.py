from marshmallow import Schema, fields


class PlainShopSchema(Schema):
    name = fields.Str(required=True)


class PlainProductSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class ShopSchemaListOutput(PlainShopSchema):
    id = fields.Integer(dump_only=True)


class ProductSchemaListOutput(PlainProductSchema):
    id = fields.Integer(dump_only=True)


class ShopSchemaIdOutput(ShopSchemaListOutput):
    datetime_create = fields.DateTime()
    datetime_update = fields.DateTime()
    products = fields.List(fields.Nested(ProductSchemaListOutput), dump_only=True)


class ProductSchemaIdOutput(ProductSchemaListOutput):
    datetime_create = fields.DateTime()
    datetime_update = fields.DateTime()
    shop = fields.Nested(ShopSchemaListOutput(), dump_only=True)
