"""poll table models update

Revision ID: dc61b0538fdc
Revises: 4b52b2e0daee
Create Date: 2024-04-06 17:54:17.661135

"""

import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from alembic import op

# revision identifiers, used by Alembic.
revision = "dc61b0538fdc"
down_revision = "4b52b2e0daee"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "poll",
        sa.Column("player_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("poll", "player_name")
    # ### end Alembic commands ###
