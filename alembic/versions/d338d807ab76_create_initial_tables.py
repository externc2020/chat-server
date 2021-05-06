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
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('nickname', sa.String(10), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.datetime('now', 'localtime')),
        sa.Column('invited_by', sa.Integer, sa.ForeignKey('users.id'), nullable=True),
        sa.Column('pubkey', sa.LargeBinary, nullable=False),
    )
    op.create_table(
        'user_friends',
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('friend_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
    )
    op.create_table(
        'rooms',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.datetime('now', 'localtime')),
    )
    op.create_table(
        'room_members',
        sa.Column('room_id', sa.Integer, sa.ForeignKey('rooms.id'), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
    )
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('room_id', sa.Integer, sa.ForeignKey('rooms.id'), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.datetime('now', 'localtime')),
    )
    op.create_table(
        'invitations',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('code', sa.String(6)),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('expired_at', sa.DateTime, nullable=False),
        sa.Column('count', sa.Integer, server_default='0'),
        sa.Column('disabled', sa.Boolean, server_default='FALSE'),
    )
    op.create_table(
        'access_tokens',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('token', sa.String(100)),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('expired_at', sa.DateTime, nullable=False),
        sa.Column('disabled', sa.Boolean, server_default='FALSE')
    )
    op.create_table(
        'refresh_tokens',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('token', sa.String(100)),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('expired_at', sa.DateTime, nullable=False),
        sa.Column('disabled', sa.Boolean, server_default='FALSE')
    )


def downgrade():
    op.drop_table('users')
    op.drop_table('user_friends')
    op.drop_table('rooms')
    op.drop_table('room_members')
    op.drop_table('messages')
