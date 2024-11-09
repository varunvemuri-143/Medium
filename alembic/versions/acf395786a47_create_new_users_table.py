"""create new users table

Revision ID: acf395786a47
Revises: 034a173d1e41
Create Date: 2024-11-09 03:10:53.421793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'acf395786a47'
down_revision = '034a173d1e41'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255)),
        sa.Column('email', sa.String(255), unique=True),
        sa.Column('hashedPassword', sa.String(255), nullable=False),
        sa.Column('user_type', sa.Enum('base', 'admin', name='user_types'), default='client'),
        sa.Column('status', sa.Enum('active', 'inactive', name='user_status'), default='active'),
        sa.Column('created_at', sa.DateTime,default=None),
        sa.Column('updated_at', sa.DateTime,default=None)
    )

    op.create_index(op.f('ix_users_email'), 'users', ['email'])
    op.create_index(op.f('ix_users_user_type'), 'users', ['user_type'])
    op.create_index(op.f('ix_users_status'), 'users', ['status'])

def downgrade():
    op.drop_table('users')
