"""add BlacklistedToken Model

Revision ID: c276f191a870
Revises: da40eec9d570
Create Date: 2022-09-01 16:05:40.339627

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c276f191a870"
down_revision = "da40eec9d570"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "token_blacklist",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("token", sa.String(length=500), nullable=False),
        sa.Column("blacklisted_on", sa.DateTime(), nullable=True),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("token_blacklist")
    # ### end Alembic commands ###
