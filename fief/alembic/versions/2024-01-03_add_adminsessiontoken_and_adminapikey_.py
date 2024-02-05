"""Add AdminSessionToken and AdminAPIKey models

Revision ID: 6d9fa141730c
Revises: 6c06c7d908a7
Create Date: 2024-01-03 15:26:46.049750

"""
import sqlalchemy as sa
from alembic import op

import fief

# revision identifiers, used by Alembic.
revision = "6d9fa141730c"
down_revision = "6c06c7d908a7"
branch_labels = None
depends_on = None


def upgrade():
    table_prefix = op.get_context().opts["table_prefix"]
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        f"{table_prefix}admin_api_key",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("token", sa.String(length=255), nullable=False),
        sa.Column("id", fief.models.generics.GUID(), nullable=False),
        sa.Column(
            "created_at",
            fief.models.generics.TIMESTAMPAware(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            fief.models.generics.TIMESTAMPAware(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token"),
    )
    op.create_index(
        op.f(f"ix_{table_prefix}admin_api_key_created_at"),
        f"{table_prefix}admin_api_key",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f(f"ix_{table_prefix}admin_api_key_updated_at"),
        f"{table_prefix}admin_api_key",
        ["updated_at"],
        unique=False,
    )
    op.create_table(
        f"{table_prefix}admin_session_tokens",
        sa.Column("token", sa.String(length=255), nullable=False),
        sa.Column("raw_tokens", sa.Text(), nullable=False),
        sa.Column("raw_userinfo", sa.Text(), nullable=False),
        sa.Column("id", fief.models.generics.GUID(), nullable=False),
        sa.Column(
            "created_at",
            fief.models.generics.TIMESTAMPAware(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            fief.models.generics.TIMESTAMPAware(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token"),
    )
    op.create_index(
        op.f(f"ix_{table_prefix}admin_session_tokens_created_at"),
        f"{table_prefix}admin_session_tokens",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f(f"ix_{table_prefix}admin_session_tokens_updated_at"),
        f"{table_prefix}admin_session_tokens",
        ["updated_at"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade():
    table_prefix = op.get_context().opts["table_prefix"]
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f(f"ix_{table_prefix}admin_session_tokens_updated_at"),
        table_name=f"{table_prefix}admin_session_tokens",
    )
    op.drop_index(
        op.f(f"ix_{table_prefix}admin_session_tokens_created_at"),
        table_name=f"{table_prefix}admin_session_tokens",
    )
    op.drop_table(f"{table_prefix}admin_session_tokens")
    op.drop_index(
        op.f(f"ix_{table_prefix}admin_api_key_updated_at"),
        table_name=f"{table_prefix}admin_api_key",
    )
    op.drop_index(
        op.f(f"ix_{table_prefix}admin_api_key_created_at"),
        table_name=f"{table_prefix}admin_api_key",
    )
    op.drop_table(f"{table_prefix}admin_api_key")
    # ### end Alembic commands ###