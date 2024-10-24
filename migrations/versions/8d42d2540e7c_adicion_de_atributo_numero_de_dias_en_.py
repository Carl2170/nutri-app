"""adicion de atributo numero de dias en healthobjetive

Revision ID: 8d42d2540e7c
Revises: 8af93c507c40
Create Date: 2024-10-23 13:52:55.746076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d42d2540e7c'
down_revision = '8af93c507c40'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('health_objective', schema=None) as batch_op:
        batch_op.add_column(sa.Column('number_days', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('health_objective', schema=None) as batch_op:
        batch_op.drop_column('number_days')

    # ### end Alembic commands ###