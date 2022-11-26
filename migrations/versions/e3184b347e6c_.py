"""empty message

Revision ID: e3184b347e6c
Revises: 47454edab16c
Create Date: 2022-02-26 20:45:42.703730

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "e3184b347e6c"
down_revision = "47454edab16c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "diary", ["category", "topic"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "diary", type_="unique")
    # ### end Alembic commands ###
