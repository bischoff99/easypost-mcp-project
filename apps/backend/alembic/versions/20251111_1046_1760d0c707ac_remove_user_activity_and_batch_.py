"""remove_user_activity_and_batch_operation_tables

Revision ID: 1760d0c707ac
Revises: fc2aec2ac737
Create Date: 2025-11-11 10:46:48.122328+00:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1760d0c707ac"
down_revision: Union[str, None] = "fc2aec2ac737"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop indexes first
    op.drop_index(op.f("ix_user_activities_user_id"), table_name="user_activities")
    op.drop_index(op.f("ix_user_activities_timestamp"), table_name="user_activities")
    op.drop_index(op.f("ix_user_activities_session_id"), table_name="user_activities")
    op.drop_index(op.f("ix_batch_operations_batch_id"), table_name="batch_operations")
    
    # Drop tables
    op.drop_table("user_activities")
    op.drop_table("batch_operations")


def downgrade() -> None:
    # Recreate batch_operations table
    op.create_table(
        "batch_operations",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("batch_id", sa.String(length=50), nullable=False),
        sa.Column("operation_type", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("total_items", sa.Integer(), nullable=False),
        sa.Column("processed_items", sa.Integer(), nullable=False),
        sa.Column("successful_items", sa.Integer(), nullable=False),
        sa.Column("failed_items", sa.Integer(), nullable=False),
        sa.Column("total_processing_time", sa.Float(), nullable=True),
        sa.Column("avg_item_time", sa.Float(), nullable=True),
        sa.Column("errors", sa.JSON(), nullable=True),
        sa.Column("user_id", sa.String(length=100), nullable=True),
        sa.Column("source", sa.String(length=50), nullable=True),
        sa.Column("parameters", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_batch_operations_batch_id"), "batch_operations", ["batch_id"], unique=True
    )
    
    # Recreate user_activities table
    op.create_table(
        "user_activities",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.String(length=100), nullable=True),
        sa.Column("session_id", sa.String(length=100), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("action", sa.String(length=100), nullable=False),
        sa.Column("resource", sa.String(length=100), nullable=True),
        sa.Column("resource_id", sa.String(length=100), nullable=True),
        sa.Column("method", sa.String(length=10), nullable=False),
        sa.Column("endpoint", sa.String(length=200), nullable=False),
        sa.Column("user_agent", sa.Text(), nullable=True),
        sa.Column("ip_address", sa.String(length=45), nullable=True),
        sa.Column("status_code", sa.Integer(), nullable=False),
        sa.Column("response_time_ms", sa.Float(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("extra_metadata", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_user_activities_session_id"), "user_activities", ["session_id"], unique=False
    )
    op.create_index(
        op.f("ix_user_activities_timestamp"), "user_activities", ["timestamp"], unique=False
    )
    op.create_index(
        op.f("ix_user_activities_user_id"), "user_activities", ["user_id"], unique=False
    )
