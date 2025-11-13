from app.core.celery_config import celery_app
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoTimeoutException, NetmikoAuthenticationException
from sqlalchemy.orm import Session
from app.database import SessionLocal # We need a way to create sessions outside FastAPI
from app.crud.config_backup import create_config_backup
import os

# --- Helper to create a DB session for the worker ---
def get_worker_db() -> Session:
    """Creates a new DB session specifically for the worker process."""
    return SessionLocal()

@celery_app.task(name="net_automation.backup_config_task")
def backup_config_task(device_id: int, device_params: dict):
    """
    Connects to a network device via Netmiko, retrieves the running config, 
    and saves the record to the database.
    """
    
    # In a real app, device_params would be fetched securely from the DB using device_id
    
    # 1. Netmiko Connection and Retrieval
    try:
        # NOTE: Using 'show run' for Cisco IOS/similar; command changes per vendor
        command = device_params.get("backup_command", "show running-config")
        
        net_connect = ConnectHandler(**device_params)
        config_data = net_connect.send_command(command)
        net_connect.disconnect()
        
        # 2. Config Storage (File System)
        # For simplicity, we save to a local file/Git repo path (Phase 2, Step 8)
        filename = f"config_{device_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.cfg"
        # In the future, this config_data would be stored in the Git repo
        
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
        return {"status": "ERROR", "message": f"Connection/Auth failed for device {device_id}: {e}"}
    except Exception as e:
        return {"status": "ERROR", "message": f"An unexpected error occurred for device {device_id}: {e}"}

    # 3. Database Record (Transactional)
    db = get_worker_db()
    try:
        backup_record = create_config_backup(db, {
            "device_id": device_id,
            "git_commit": "TBD_Phase_8", # Placeholder for Git commit hash
            "diff_summary": f"Successful backup captured ({len(config_data)} bytes)",
            # In Phase 8, we would also save the file and commit the change to Git
        })
        return {
            "status": "SUCCESS", 
            "message": f"Backup successful. DB ID: {backup_record.id}",
            "config_length": len(config_data)
        }
    except Exception as db_e:
        return {"status": "ERROR", "message": f"Backup succeeded but DB record failed: {db_e}"}
    finally:
        db.close()

# Example Call Simulation (Run this in a test environment)
from datetime import datetime
if __name__ == '__main__':
    # Simulating data fetched from the DB (Device and Credential models)
    sample_device = {
        "device_type": "cisco_ios",
        "host": "192.168.1.1",
        "username": "snams_user",
        "password": "secure_password",
        "secret": "enable_secret"
    }
    # backup_config_task.delay(1, sample_device) # Use .delay() to queue the task
    print("Task would be queued if Celery worker was running.")
