"""poll table models

Revision ID: 4b52b2e0daee
Revises: e2412789c190
Create Date: 2024-04-06 00:00:10.131324

"""

import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from alembic import op

# revision identifiers, used by Alembic.
revision = "4b52b2e0daee"
down_revision = "e2412789c190"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "poll",
        sa.Column("hero_id", sa.Integer(), nullable=False),
        sa.Column("hero_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("team", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("poll")
    # ### end Alembic commands ###
