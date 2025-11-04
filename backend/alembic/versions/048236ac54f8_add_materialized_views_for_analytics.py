"""add_materialized_views_for_analytics

Revision ID: 048236ac54f8
Revises: 73e8f9a2b1c4
Create Date: 2025-11-04 10:07:41.753296+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '048236ac54f8'
down_revision: Union[str, None] = '73e8f9a2b1c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create materialized views for fast analytics queries."""
    
    # =========================================================================
    # MATERIALIZED VIEW 1: Daily Shipment Analytics
    # =========================================================================
    op.execute("""
        CREATE MATERIALIZED VIEW IF NOT EXISTS mv_daily_shipment_analytics AS
        SELECT
            DATE(created_at) as date,
            carrier,
            service,
            COUNT(*) as shipment_count,
            SUM(total_cost) as total_cost,
            AVG(total_cost) as avg_cost,
            COUNT(CASE WHEN status = 'delivered' THEN 1 END) as delivered_count,
            COUNT(CASE WHEN status IN ('in_transit', 'pre_transit') THEN 1 END) as in_transit_count,
            COUNT(CASE WHEN status IN ('failure', 'cancelled') THEN 1 END) as failed_count,
            AVG(delivery_days) as avg_delivery_days,
            MIN(created_at) as first_shipment_time,
            MAX(created_at) as last_shipment_time
        FROM shipments
        WHERE created_at >= CURRENT_DATE - INTERVAL '90 days'
        GROUP BY DATE(created_at), carrier, service
        ORDER BY date DESC, shipment_count DESC;
    """)
    
    # Create indexes on materialized view
    op.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS ix_mv_daily_analytics_date_carrier_service
        ON mv_daily_shipment_analytics (date, carrier, service);
    """)
    
    op.execute("""
        CREATE INDEX IF NOT EXISTS ix_mv_daily_analytics_date
        ON mv_daily_shipment_analytics (date DESC);
    """)
    
    # =========================================================================
    # MATERIALIZED VIEW 2: Carrier Performance Summary
    # =========================================================================
    op.execute("""
        CREATE MATERIALIZED VIEW IF NOT EXISTS mv_carrier_performance AS
        SELECT
            carrier,
            service,
            COUNT(*) as total_shipments,
            SUM(total_cost) as total_revenue,
            AVG(total_cost) as avg_cost,
            COUNT(CASE WHEN status = 'delivered' THEN 1 END) as delivered_count,
            COUNT(CASE WHEN status IN ('delivered', 'returned', 'cancelled') THEN 1 END) as completed_count,
            CASE 
                WHEN COUNT(CASE WHEN status IN ('delivered', 'returned', 'cancelled') THEN 1 END) > 0
                THEN (COUNT(CASE WHEN status = 'delivered' THEN 1 END)::float / 
                      COUNT(CASE WHEN status IN ('delivered', 'returned', 'cancelled') THEN 1 END) * 100)
                ELSE 95.0
            END as on_time_rate,
            AVG(delivery_days) as avg_delivery_days,
            MIN(created_at) as first_shipment,
            MAX(created_at) as last_shipment,
            MAX(updated_at) as last_updated
        FROM shipments
        WHERE created_at >= CURRENT_DATE - INTERVAL '90 days'
        GROUP BY carrier, service
        ORDER BY total_shipments DESC;
    """)
    
    # Create indexes on carrier performance view
    op.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS ix_mv_carrier_performance_carrier_service
        ON mv_carrier_performance (carrier, service);
    """)
    
    # =========================================================================
    # MATERIALIZED VIEW 3: Top Routes
    # =========================================================================
    op.execute("""
        CREATE MATERIALIZED VIEW IF NOT EXISTS mv_top_routes AS
        SELECT
            fa.city as from_city,
            fa.state as from_state,
            fa.country as from_country,
            ta.city as to_city,
            ta.state as to_state,
            ta.country as to_country,
            COUNT(s.id) as shipment_count,
            SUM(s.total_cost) as total_cost,
            AVG(s.total_cost) as avg_cost,
            AVG(s.delivery_days) as avg_delivery_days,
            MAX(s.created_at) as last_shipment
        FROM shipments s
        JOIN addresses fa ON s.from_address_id = fa.id
        JOIN addresses ta ON s.to_address_id = ta.id
        WHERE s.created_at >= CURRENT_DATE - INTERVAL '90 days'
        GROUP BY fa.city, fa.state, fa.country, ta.city, ta.state, ta.country
        HAVING COUNT(s.id) >= 3
        ORDER BY shipment_count DESC
        LIMIT 100;
    """)
    
    # Create index on top routes
    op.execute("""
        CREATE INDEX IF NOT EXISTS ix_mv_top_routes_count
        ON mv_top_routes (shipment_count DESC);
    """)
    
    # =========================================================================
    # REFRESH FUNCTION: Auto-refresh materialized views
    # =========================================================================
    op.execute("""
        CREATE OR REPLACE FUNCTION refresh_analytics_views()
        RETURNS void AS $$
        BEGIN
            REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_shipment_analytics;
            REFRESH MATERIALIZED VIEW CONCURRENTLY mv_carrier_performance;
            REFRESH MATERIALIZED VIEW CONCURRENTLY mv_top_routes;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # Add comment
    op.execute("""
        COMMENT ON FUNCTION refresh_analytics_views() IS
        'Refresh all analytics materialized views. Run hourly via cron or pg_cron.';
    """)


def downgrade() -> None:
    """Drop materialized views and refresh function."""
    
    # Drop refresh function
    op.execute("DROP FUNCTION IF EXISTS refresh_analytics_views()")
    
    # Drop materialized views
    op.execute("DROP MATERIALIZED VIEW IF EXISTS mv_top_routes")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS mv_carrier_performance")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS mv_daily_shipment_analytics")
