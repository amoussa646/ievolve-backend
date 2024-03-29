"""Initial migration

Revision ID: 1b203edc11c4
Revises: c702a2a3d8e5
Create Date: 2024-03-01 15:22:42.203806

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1b203edc11c4"
down_revision = "c702a2a3d8e5"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("habit", sa.Column("frequency", sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("habit", "frequency")
    # ### end Alembic commands ###
