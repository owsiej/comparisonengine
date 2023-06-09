"""empty message

Revision ID: 2153a755c84b
Revises: d3e8fc196b6e
Create Date: 2023-04-11 13:05:21.399408

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2153a755c84b'
down_revision = 'd3e8fc196b6e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tags', schema=None) as batch_op:
        batch_op.drop_constraint('uq_tags_name', type_='unique')
        batch_op.drop_constraint('fk_tags_shop_id_shops', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_tags_shop_id_shops'), 'shops', ['shop_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')

    with op.batch_alter_table('tags_products', schema=None) as batch_op:
        batch_op.drop_constraint('fk_tags_products_product_id_products', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_tags_products_product_id_products'), 'products', ['product_id'], ['id'], onupdate='CASCADE', ondelete='RESTRICT')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tags_products', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_tags_products_product_id_products'), type_='foreignkey')
        batch_op.create_foreign_key('fk_tags_products_product_id_products', 'products', ['product_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')

    with op.batch_alter_table('tags', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_tags_shop_id_shops'), type_='foreignkey')
        batch_op.create_foreign_key('fk_tags_shop_id_shops', 'shops', ['shop_id'], ['id'], onupdate='CASCADE')
        batch_op.create_unique_constraint('uq_tags_name', ['name'])

    # ### end Alembic commands ###
