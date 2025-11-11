# Database Migration Strategy

This document outlines the database migration strategy for the EasyPost MCP project.

## Migration Tool

**Alembic** - SQLAlchemy database migration tool

**Configuration**: `apps/backend/alembic.ini`
**Migrations Directory**: `apps/backend/alembic/versions/`

## Current Migration Status

### Active Migrations

1. `7e2202dec93c_initial_schema.py` - Initial database schema
2. `72c02b9d8f35_add_all_models.py` - Add all SQLAlchemy models
3. `73e8f9a2b1c4_optimize_indexes_and_uuid_v7.py` - Optimize indexes and UUID v7
4. `41963d524981_make_parcel_id_nullable.py` - Make parcel_id nullable
5. `fc2aec2ac737_update_timestamp_defaults_to_server_side.py` - Server-side timestamp defaults
6. `20251111_1046_1760d0c707ac_remove_user_activity_and_batch_.py` - Remove user activity and batch tables (personal-use simplification)

### Removed Migrations

- `048236ac54f8_add_materialized_views_for_analytics.py` - **Removed** (enterprise feature, not needed for personal use)

## Migration Commands

### Check Current Migration

```bash
cd apps/backend
source venv/bin/activate  # or .venv/bin/activate
alembic current
```

### Create New Migration

```bash
cd apps/backend
alembic revision --autogenerate -m "description of changes"
```

### Apply Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Apply specific migration
alembic upgrade <revision_id>

# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>
```

### Review Migration History

```bash
# Show migration history
alembic history

# Show current revision
alembic current
```

## Migration Best Practices

### 1. Always Review Auto-Generated Migrations

Alembic's `--autogenerate` is helpful but not perfect:

```bash
# Generate migration
alembic revision --autogenerate -m "add new field"

# Review the generated file in alembic/versions/
# Edit if needed before applying
```

### 2. Test Migrations Locally First

```bash
# Reset local database
make db-reset

# Apply migrations
make db-upgrade

# Verify schema
alembic current
```

### 3. Backup Before Production Migrations

```bash
# Backup database before migration
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Apply migration
alembic upgrade head

# Verify application works
```

### 4. Use Descriptive Migration Names

Good names:
- `add_shipment_tracking_index`
- `remove_enterprise_features`
- `make_email_nullable`

Bad names:
- `update`
- `fix`
- `changes`

## Migration Workflow

### Development

1. Modify SQLAlchemy models in `apps/backend/src/models/`
2. Generate migration: `alembic revision --autogenerate -m "description"`
3. Review generated migration file
4. Test locally: `alembic upgrade head`
5. Commit migration file with model changes

### Production

1. Backup database
2. Review migration in staging environment
3. Apply migration: `alembic upgrade head`
4. Verify application functionality
5. Monitor for issues

## Personal-Use Simplifications

As part of the personal-use simplification, the following migrations were removed:

- **Materialized views for analytics** - Removed complex analytics features
- **User activity tracking** - Removed user activity tables
- **Batch operations** - Removed batch processing tables

These removals are documented in migration `20251111_1046_1760d0c707ac_remove_user_activity_and_batch_.py`.

## Troubleshooting

### Migration Conflicts

If migrations conflict:

```bash
# Check current state
alembic current

# Review history
alembic history

# Manually resolve conflicts in migration files
```

### Failed Migrations

If a migration fails:

```bash
# Check migration status
alembic current

# Review error logs
# Fix the migration file
# Re-run: alembic upgrade head
```

### Database Out of Sync

If database is out of sync with models:

```bash
# Reset database (development only!)
make db-reset

# Or manually:
alembic downgrade base
alembic upgrade head
```

## Related Documentation

- `docs/architecture/POSTGRESQL_ARCHITECTURE.md` - Database architecture details
- `apps/backend/src/models/` - SQLAlchemy model definitions
- `apps/backend/src/database.py` - Database connection setup

## Migration Checklist

Before creating a migration:
- [ ] Model changes are tested locally
- [ ] Migration name is descriptive
- [ ] Migration is reviewed for correctness
- [ ] Migration is tested on clean database
- [ ] Migration is tested on existing data

Before applying in production:
- [ ] Database backup created
- [ ] Migration tested in staging
- [ ] Rollback plan documented
- [ ] Application tested after migration
- [ ] Monitoring in place
