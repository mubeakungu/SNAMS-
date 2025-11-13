from sqlalchemy.orm import Session
from app.models.device import Device
from app.schemas.device import DeviceCreate
from typing import List, Optional

def get_device(db: Session, device_id: int) -> Optional[Device]:
    """Retrieves a single device by its primary key ID."""
    return db.query(Device).filter(Device.id == device_id).first()

def get_device_by_ip(db: Session, ip: str) -> Optional[Device]:
    """Retrieves a single device by its IP address."""
    return db.query(Device).filter(Device.ip == ip).first()

def get_devices(db: Session, skip: int = 0, limit: int = 100) -> List[Device]:
    """Retrieves a list of devices with pagination."""
    return db.query(Device).offset(skip).limit(limit).all()

def create_device(db: Session, device: DeviceCreate) -> Device:
    """Creates a new device entry in the database."""
    # Convert the Pydantic model to a dict for easy model instantiation
    db_device = Device(**device.model_dump())
    
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

# Future functions will include update_device and delete_device
# For now, this covers the critical Read/Create functions for the MVP.
