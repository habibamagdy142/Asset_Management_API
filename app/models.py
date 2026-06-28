from datetime import datetime
from sqlalchemy import Table, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from .database import Base
from sqlalchemy import Index

asset_relationships = Table(
    "asset_relationships",
    Base.metadata,

    Column(
        "source_id",
        String,
        ForeignKey("assets.id")
    ),

    Column(
        "target_id",
        String,
        ForeignKey("assets.id")
    )
)


class Asset(Base):
    __tablename__ = "assets"

    __table_args__ = (
        Index("ix_assets_type_value", "type", "value"),
        Index("ix_assets_status", "status"),
    )

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )


    type = Column(
        String,
        nullable=False
    )


    value = Column(
        String,
        nullable=False,
        index=True
    )


    status = Column(
        String,
        default="active"
    )


    first_seen = Column(
        DateTime,
        default=datetime.utcnow
    )

    last_seen = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


    source = Column(String)


    tags = Column(JSONB)

    asset_metadata = Column(
        "metadata",
        JSONB
    )
    related_assets = relationship(
        "Asset",
        secondary=asset_relationships,
        primaryjoin=id == asset_relationships.c.source_id,
        secondaryjoin=id == asset_relationships.c.target_id
    )