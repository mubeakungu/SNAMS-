# app/crud/config_backup.py

from sqlalchemy.orm import Session
from app.models.device import ConfigBackup
from datetime import datetime
from typing import Dict, Any

def create_config_backup(db: Session, backup_data: Dict[str, Any]) -> ConfigBackup:
    """Records a new configuration backup entry in the database."""
    # backup_data should contain: device_id, git_commit, diff_summary, backup_path
    db_backup = ConfigBackup(
        device_id=backup_data.get("device_id"),
        git_commit=backup_data.get("git_commit"),
        diff_summary=backup_data.get("diff_summary"),
        # We need to add 'backup_path' to the ConfigBackup model later 
        # for a complete solution, but will omit it for now for simplicity.
        timestamp=datetime.utcnow()
    )
    db.add(db_backup)
    db.commit()
    db.refresh(db_backup)
    return db_backup
