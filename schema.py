from marshmallow import Schema, fields


class PlainShopSchema(Schema):
    name = fields.Str(required=True)


class PlainProductSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class PlainTagSchema(Schema):
    name = fields.Str(required=True)


class ShopSchemaListOutput(PlainShopSchema):
    id = fields.Integer(dump_only=True)


class ProductSchemaListOutput(PlainProductSchema):
    id = fields.Integer(dump_only=True)
    shop_id = fields.Integer()


class TagSchemaListOutput(PlainTagSchema):
    id = fields.Integer(dump_only=True)
    shop_id = fields.Integer()


class ShopSchemaIdOutput(ShopSchemaListOutput):
    datetime_create = fields.DateTime(dump_only=True)
    datetime_update = fields.DateTime(dump_only=True)
    products = fields.List(fields.Nested(ProductSchemaListOutput), dump_only=True)
    tags = fields.List(fields.Nested(TagSchemaListOutput), dump_only=True)


class ProductSchemaIdOutput(ProductSchemaListOutput):
    datetime_create = fields.DateTime(dump_only=True)
    datetime_update = fields.DateTime(dump_only=True)
    shop = fields.Nested(ShopSchemaListOutput(), dump_only=True)
    tags = fields.List(fields.Nested(TagSchemaListOutput), dump_only=True)


class TagSchemaIdOutPut(TagSchemaListOutput):
    datetime_create = fields.DateTime(dump_only=True)
    datetime_update = fields.DateTime(dump_only=True)
    shop = fields.Nested(ShopSchemaListOutput(), dump_only=True)
    products = fields.List(fields.Nested(ProductSchemaListOutput(), dump_only=True))


class TagsProducts(Schema):
    message = fields.Str()
    tag = fields.Nested(TagSchemaIdOutPut)
    product = fields.Nested(ProductSchemaIdOutput)


class ProductSchemaUpdate(Schema):
    name = fields.Str()
    price = fields.Float()
