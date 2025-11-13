from sqlalchemy import String, Boolean, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from datetime import datetime
import enum
from typing import Optional

# --- Enums ---
class UserRole(str, enum.Enum):
    Admin = "Admin"
    Engineer = "Engineer"
    ReadOnly = "ReadOnly"

class User(Base):
    """Represents a user account for the SNAMS platform."""
    __tablename__ = "snams_user" # Use snams_user to avoid conflict with 'user' keyword in some DBs

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    email: Mapped[Optional[str]] = mapped_column(String(128))
    hashed_password: Mapped[str] = mapped_column(String(128))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.ReadOnly)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
