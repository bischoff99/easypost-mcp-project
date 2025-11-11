"""Optimize indexes and add UUID v7 support

Revision ID: 73e8f9a2b1c4
Revises: 41963d524981
Create Date: 2025-11-04 12:00:00.000000

This migration:
1. Adds uuid-ossp extension for UUID v7 generation
2. Creates composite indexes for common query patterns
3. Adds INCLUDE indexes for covering queries
4. Optimizes existing indexes

"""
from collections.abc import Sequence
from typing import Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '73e8f9a2b1c4'
down_revision: Union[str, None] = '41963d524981'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enable uuid-ossp extension for UUID v7
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # Add function for UUID v7 generation (time-ordered UUIDs)
    # Based on RFC 4122 draft for UUID v7
    op.execute("""
        CREATE OR REPLACE FUNCTION uuid_generate_v7()
        RETURNS uuid
        AS $$
        DECLARE
            unix_ts_ms bytea;
            uuid_bytes bytea;
        BEGIN
            unix_ts_ms = substring(int8send(floor(extract(epoch from clock_timestamp()) * 1000)::bigint) from 3);
            uuid_bytes = unix_ts_ms || gen_random_bytes(10);
            RETURN encode(
                overlay(uuid_bytes placing get_byte(uuid_bytes, 6)::bit(8)::bit(4) || '0111'::bit(4) from 7 for 1) ||
                overlay(uuid_bytes placing '10'::bit(2) || substring(get_byte(uuid_bytes, 8)::bit(8) from 3) from 9 for 1),
                'hex'
            )::uuid;
        END
        $$ LANGUAGE plpgsql VOLATILE;
    """)

    # ========================================================================
    # COMPOSITE INDEXES FOR COMMON QUERY PATTERNS
    # ========================================================================

    # Shipments: filter by carrier + service + date range
    op.create_index(
        'ix_shipments_carrier_service_created',
        'shipments',
        ['carrier', 'service', 'created_at'],
        unique=False,
        postgresql_using='btree'
    )

    # Shipments: filter by status + date range
    op.create_index(
        'ix_shipments_status_created',
        'shipments',
        ['status', 'created_at'],
        unique=False,
        postgresql_using='btree'
    )

    # Shipments: destination-based lookups by date
    op.create_index(
        'ix_shipments_to_address_created',
        'shipments',
        ['to_address_id', 'created_at'],
        unique=False,
        postgresql_using='btree'
    )

    # ========================================================================
    # INCLUDE INDEXES (Covering Indexes for Performance)
    # ========================================================================

    # Tracking: covering index to avoid table lookup
    op.execute("""
        CREATE INDEX IF NOT EXISTS ix_shipments_tracking_covering
        ON shipments (tracking_code)
        INCLUDE (status, carrier, service, updated_at)
    """)

    # Shipment events: covering index for timeline queries
    op.execute("""
        CREATE INDEX IF NOT EXISTS ix_shipment_events_covering
        ON shipment_events (shipment_id, event_datetime DESC)
        INCLUDE (status, message, carrier_status)
    """)

    # ========================================================================
    # PARTIAL INDEXES FOR COMMON FILTERS
    # ========================================================================

    # Active shipments only (status not 'delivered' or 'cancelled')
    op.execute("""
        CREATE INDEX IF NOT EXISTS ix_shipments_active
        ON shipments (created_at DESC)
        WHERE status NOT IN ('delivered', 'cancelled', 'returned')
    """)

    # Failed shipments for monitoring
    op.execute("""
        CREATE INDEX IF NOT EXISTS ix_shipments_failed
        ON shipments (created_at DESC)
        WHERE status IN ('failure', 'error', 'cancelled')
    """)

    # ========================================================================
    # ANALYTICS TABLE INDEXES
    # ========================================================================
    # Note: Analytics indexes will be added when analytics table is created

    # ========================================================================
    # ADD COMMENTS FOR DOCUMENTATION
    # ========================================================================

    op.execute("""
        COMMENT ON FUNCTION uuid_generate_v7() IS
        'Generate time-ordered UUID v7 for better B-tree locality and insert performance'
    """)


def downgrade() -> None:
    # Drop custom indexes
    op.execute('DROP INDEX IF EXISTS ix_shipments_failed')
    op.execute('DROP INDEX IF EXISTS ix_shipments_active')
    op.execute('DROP INDEX IF EXISTS ix_shipment_events_covering')
    op.execute('DROP INDEX IF EXISTS ix_shipments_tracking_covering')
    op.drop_index('ix_shipments_to_address_created', table_name='shipments')
    op.drop_index('ix_shipments_status_created', table_name='shipments')
    op.drop_index('ix_shipments_carrier_service_created', table_name='shipments')

    # Drop UUID v7 function
    op.execute('DROP FUNCTION IF EXISTS uuid_generate_v7()')

    # Note: We don't drop uuid-ossp extension as it might be used elsewhere

