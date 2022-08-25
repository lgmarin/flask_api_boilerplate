"""Add User model

Revision ID: 2980d6275529
Revises: 
Create Date: 2022-08-25 10:53:39.133396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2980d6275529"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "app_user",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=100), nullable=False),
        sa.Column("registered_on", sa.DateTime(), nullable=True),
        sa.Column("admin", sa.Boolean(), nullable=True),
        sa.Column("public_id", sa.String(length=36), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("public_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("app_user")
    # ### end Alembic commands ###
