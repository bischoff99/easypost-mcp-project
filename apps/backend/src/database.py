"""
Database stub for personal use (database removed).

This module provides minimal SQLAlchemy Base class to prevent import errors.
Database models exist but are not used - all data is retrieved directly from EasyPost API.
"""

from sqlalchemy.orm import declarative_base

# Minimal Base class to satisfy imports (not actually used)
Base = declarative_base()
