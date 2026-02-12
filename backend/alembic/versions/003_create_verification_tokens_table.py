"""Create verification_tokens table

Revision ID: 003
Revises: 002
Create Date: 2026-02-06 12:10:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create verification_tokens table for password reset."""
    op.create_table(
        'verification_tokens',
        sa.Column('identifier', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column('token', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column('expires', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('identifier', 'token')
    )
    op.create_index(op.f('ix_verification_tokens_token'), 'verification_tokens', ['token'], unique=True)


def downgrade() -> None:
    """Drop verification_tokens table."""
    op.drop_index(op.f('ix_verification_tokens_token'), table_name='verification_tokens')
    op.drop_table('verification_tokens')
