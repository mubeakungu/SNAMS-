from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.models.device import InterfaceStatus # Re-use the enum

class DeviceBase(BaseModel):
    hostname: str
    vendor: str
    model: Optional[str] = None
    ip: str
    management_ip: Optional[str] = None
    credentials_ref: Optional[str] = None
    is_active: bool = True

class DeviceCreate(DeviceBase):
    # Only fields required for creation
    pass

class InterfaceSchema(BaseModel):
    name: str
    index: int
    status: InterfaceStatus

class Device(DeviceBase):
    # Fields that come from the database
    model_config = ConfigDict(from_attributes=True) # Enables ORM mode

    id: int
    last_seen: Optional[datetime] = None
    created_at: datetime
    # Nested schemas for relationships (optional for MVP, but good practice)
    interfaces: List[InterfaceSchema] = []
