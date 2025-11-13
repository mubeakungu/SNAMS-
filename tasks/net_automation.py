from app.core.celery_config import celery_app
from time import sleep # Used for simulation

@celery_app.task(name="net_automation.backup_config_task")
def backup_config_task(device_id: int):
    """
    SIMULATION: A task to simulate a config backup process.
    
    This function will be expanded in Phase 2, Step 7 using Netmiko.
    """
    print(f"Starting config backup for Device ID: {device_id}")
    
    # Simulate the time delay of connecting to a device
    sleep(5) 
    
    # In a real scenario, this would return the success status, file path, etc.
    return {"status": "SUCCESS", "device_id": device_id, "message": "Config backup completed."}

# Other tasks (deploy, discovery, monitoring) will be added here later.
