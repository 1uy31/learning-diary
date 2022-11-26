"""empty message

Revision ID: 47454edab16c
Revises:
Create Date: 2022-02-20 07:53:44.440181

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "47454edab16c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "category",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "note",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "position",
            sa.SmallInteger(),
            nullable=False,
            comment="The position of each note in a diary.",
        ),
        sa.Column("text", sa.Text(), nullable=True),
        sa.Column("image_url", sa.String(length=256), nullable=True),
        sa.Column("source_url", sa.String(length=256), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("position"),
    )
    op.create_table(
        "diary",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("topic", sa.String(), nullable=False),
        sa.Column("category", sa.Integer(), nullable=True),
        sa.Column("note", sa.Integer(), nullable=True),
        sa.Column("source_url", sa.String(length=256), nullable=True),
        sa.Column("review_count", sa.SmallInteger(), nullable=True),
        sa.Column("rate", sa.SmallInteger(), nullable=True),
        sa.ForeignKeyConstraint(["category"], ["category.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["note"], ["note.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("diary")
    op.drop_table("note")
    op.drop_table("category")
    # ### end Alembic commands ###