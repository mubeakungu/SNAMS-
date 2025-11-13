from sqlalchemy import String, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
from datetime import datetime
import enum
from typing import List, Optional

# --- Enums (Mapped from SQL) ---
class InterfaceStatus(str, enum.Enum):
    """Defines the operational status of a network interface."""
    up = "up"
    down = "down"
    admin_down = "admin_down"

# --- Models ---
class Device(Base):
    """Represents a network device in the inventory."""
    __tablename__ = "device"

    id: Mapped[int] = mapped_column(primary_key=True)
    hostname: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    vendor: Mapped[str] = mapped_column(String(64), index=True)
    model: Mapped[Optional[str]] = mapped_column(String(64))
    ip: Mapped[str] = mapped_column(String, unique=True)
    credentials_ref: Mapped[Optional[str]] = mapped_column(String)
    last_seen: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationships: Back-populates define the link from the related model back here
    interfaces: Mapped[List["Interface"]] = relationship(back_populates="device", cascade="all, delete-orphan")
    backups: Mapped[List["ConfigBackup"]] = relationship(back_populates="device", cascade="all, delete-orphan")


class Interface(Base):
    """Represents a physical or logical interface on a device."""
    __tablename__ = "interface"

    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("device.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(64))
    index: Mapped[int] = mapped_column() # SNMP ifIndex

    status: Mapped[InterfaceStatus] = mapped_column(Enum(InterfaceStatus), default=InterfaceStatus.admin_down)
    
    # Relationship
    device: Mapped["Device"] = relationship(back_populates="interfaces")

    # Composite unique constraints
    __table_args__ = (
        # Ensure name is unique per device (e.g., Gig0/1)
        {"unique_together": (("device_id", "name"),)}
    )

class ConfigBackup(Base):
    """Represents a versioned configuration snapshot."""
    __tablename__ = "config_backup"

    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("device.id", ondelete="CASCADE"), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    git_commit: Mapped[str] = mapped_column(String(40), unique=True) # SHA-1 hash
    diff_summary: Mapped[Optional[str]] = mapped_column(Text)
    
    # Relationship
    device: Mapped["Device"] = relationship(back_populates="backups")
