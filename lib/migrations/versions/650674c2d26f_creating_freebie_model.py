"""Creating Freebie Model

Revision ID: 650674c2d26f
Revises: 5f72c58bf48c
Create Date: 2023-12-13 14:37:37.731967

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '650674c2d26f'
down_revision = '5f72c58bf48c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('freebies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_name', sa.String(), nullable=True),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('dev_id', sa.Integer(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], name=op.f('fk_freebies_company_id_companies')),
    sa.ForeignKeyConstraint(['dev_id'], ['devs.id'], name=op.f('fk_freebies_dev_id_devs')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('freebies')
    # ### end Alembic commands ###
