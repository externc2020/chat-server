"""create initial tables

Revision ID: d338d807ab76
Revises: 
Create Date: 2021-05-06 14:34:08.641912

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd338d807ab76'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('pubkey', sa.String, primary_key=True),
    )
    op.create_table(
        'chunks',
        sa.Column('digest', sa.String, primary_key=True),
        sa.Column('data', sa.LargeBinary),
    )
    op.create_table(
        'chunk_graph',
        sa.Column('from', sa.String),
        sa.Column('to', sa.String),
    )
    op.execute("INSERT INTO users (pubkey) VALUES ('ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGqEfouHdAJzWSgqbeImhz1X8H9mB8YetzMRGGtxFJqc')")


def downgrade():
    op.drop_table('users')
    op.drop_table('chunks')
    op.drop_table('chunk_graph')
