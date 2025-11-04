"""
Database models for shipments and related entities.
"""

import uuid
from datetime import datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..database import Base


class Shipment(Base):
    """Shipment model for storing EasyPost shipment data."""

    __tablename__ = "shipments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    easypost_id = Column(String(50), unique=True, index=True, nullable=False)
    tracking_code = Column(String(100), index=True, nullable=True)
    status = Column(String(50), nullable=False, default="unknown")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Shipment details
    mode = Column(String(20), nullable=False, default="test")  # test/live
    reference = Column(String(100), nullable=True)

    # Addresses
    from_address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.id"), nullable=False)
    to_address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.id"), nullable=False)
    return_address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.id"), nullable=True)
    buyer_address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.id"), nullable=True)

    # Parcel
    parcel_id = Column(UUID(as_uuid=True), ForeignKey("parcels.id"), nullable=True)

    # Customs info
    customs_info_id = Column(UUID(as_uuid=True), ForeignKey("customs_infos.id"), nullable=True)

    # Rates and selection
    selected_rate_id = Column(String(50), nullable=True)
    rates_data = Column(JSON, nullable=True)  # Store all rates from EasyPost

    # Costs
    base_cost = Column(Float, nullable=True)
    total_cost = Column(Float, nullable=True)
    currency = Column(String(3), nullable=False, default="USD")

    # Carrier and service
    carrier = Column(String(50), nullable=True)
    service = Column(String(50), nullable=True)
    delivery_days = Column(Integer, nullable=True)
    delivery_date = Column(DateTime, nullable=True)

    # Tracking
    tracking_details = Column(JSON, nullable=True)  # Store tracking history
    signed_by = Column(String(100), nullable=True)
    weight = Column(Float, nullable=True)  # Actual weight used
    est_delivery_date = Column(DateTime, nullable=True)

    # Metadata
    extra_metadata = Column(JSON, nullable=True)
    batch_id = Column(String(50), nullable=True)  # For batch operations
    batch_status = Column(String(20), nullable=True)

    # Relationships
    from_address = relationship("Address", foreign_keys=[from_address_id])
    to_address = relationship("Address", foreign_keys=[to_address_id])
    return_address = relationship("Address", foreign_keys=[return_address_id])
    buyer_address = relationship("Address", foreign_keys=[buyer_address_id])
    parcel = relationship("Parcel", back_populates="shipments")
    customs_info = relationship("CustomsInfo", back_populates="shipments")

    def __repr__(self):
        return f"<Shipment(id={self.id}, tracking={self.tracking_code}, status={self.status})>"


class Address(Base):
    """Address model for storing shipping addresses."""

    __tablename__ = "addresses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    easypost_id = Column(String(50), unique=True, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Address fields
    name = Column(String(100), nullable=True)
    company = Column(String(100), nullable=True)
    street1 = Column(String(200), nullable=False)
    street2 = Column(String(200), nullable=True)
    city = Column(String(100), nullable=False)
    state = Column(String(50), nullable=True)
    zip = Column(String(20), nullable=False)
    country = Column(String(2), nullable=False, default="US")  # ISO 3166-1 alpha-2
    phone = Column(String(20), nullable=True)
    email = Column(String(200), nullable=True)

    # Verification
    verifications = Column(JSON, nullable=True)

    # Metadata
    is_residential = Column(Boolean, nullable=True)
    carrier_facility = Column(String(50), nullable=True)
    federal_tax_id = Column(String(20), nullable=True)
    state_tax_id = Column(String(20), nullable=True)

    def __repr__(self):
        return f"<Address(id={self.id}, city={self.city}, country={self.country})>"


class Parcel(Base):
    """Parcel model for storing package dimensions and weight."""

    __tablename__ = "parcels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    easypost_id = Column(String(50), unique=True, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Dimensions
    length = Column(Float, nullable=True)
    width = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=False)  # in ounces
    predefined_package = Column(String(50), nullable=True)

    # Additional properties
    mass_unit = Column(String(10), nullable=False, default="oz")
    distance_unit = Column(String(10), nullable=False, default="in")

    # Relationships
    shipments = relationship("Shipment", back_populates="parcel")

    def __repr__(self):
        return f"<Parcel(id={self.id}, weight={self.weight} {self.mass_unit})>"


class CustomsInfo(Base):
    """Customs information for international shipments."""

    __tablename__ = "customs_infos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    easypost_id = Column(String(50), unique=True, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Customs declaration
    contents_type = Column(String(50), nullable=False, default="merchandise")
    contents_explanation = Column(Text, nullable=True)
    customs_certify = Column(Boolean, nullable=False, default=True)
    customs_signer = Column(String(100), nullable=True)
    non_delivery_option = Column(String(20), nullable=False, default="return")
    restriction_type = Column(String(20), nullable=False, default="none")
    restriction_comments = Column(Text, nullable=True)
    customs_items = Column(JSON, nullable=True)  # Store customs items array

    # EEL/PFC
    eel_pfc = Column(String(20), nullable=True)

    # Relationships
    shipments = relationship("Shipment", back_populates="customs_info")

    def __repr__(self):
        return f"<CustomsInfo(id={self.id}, contents_type={self.contents_type})>"


class ShipmentEvent(Base):
    """Tracking events for shipments."""

    __tablename__ = "shipment_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shipment_id = Column(UUID(as_uuid=True), ForeignKey("shipments.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Event details
    status = Column(String(50), nullable=False)
    message = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    carrier_status = Column(String(100), nullable=True)
    tracking_location = Column(JSON, nullable=True)  # city, state, country, zip

    # Timestamps
    event_datetime = Column(DateTime, nullable=False)

    def __repr__(self):
        return (
            f"<ShipmentEvent(id={self.id}, status={self.status}, datetime={self.event_datetime})>"
        )
