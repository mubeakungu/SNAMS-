from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import device as device_schemas
from app.crud import device as device_crud
from app.core.security import get_current_user # To protect routes later (placeholder)

# Initialize the router
router = APIRouter(tags=["Devices"])

@router.post("/devices", response_model=device_schemas.Device, status_code=status.HTTP_201_CREATED)
def create_new_device(
    device: device_schemas.DeviceCreate, 
    db: Session = Depends(get_db)
    # user: dict = Depends(get_current_user) # Uncomment to require authentication
):
    """Adds a new network device to the inventory."""
    # 1. Check for existing device by IP
    db_device = device_crud.get_device_by_ip(db, ip=device.ip)
    if db_device:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Device with IP {device.ip} already exists."
        )
    
    # 2. Create the device
    return device_crud.create_device(db=db, device=device)

@router.get("/devices", response_model=List[device_schemas.Device])
def read_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieves a list of devices in the inventory with pagination."""
    devices = device_crud.get_devices(db, skip=skip, limit=limit)
    return devices

@router.get("/devices/{device_id}", response_model=device_schemas.Device)
def read_device(device_id: int, db: Session = Depends(get_db)):
    """Retrieves details for a specific device by ID."""
    db_device = device_crud.get_device(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    return db_device
