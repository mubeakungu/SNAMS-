from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import verify_password, create_access_token
from app.models.token import Token
# Import the User model from app.models.user
from app.models.user import User

router = APIRouter(tags=["Authentication"])

# Helper function (will be placed in a 'crud' module later)
def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Retrieves and validates a user's password."""
    # NOTE: This uses the model defined in Phase 1, Step 3
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """
    Standard OAuth2 endpoint to exchange username and password for a JWT token.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create the token payload including the user's role for RBAC
    access_token_expires = timedelta(minutes=config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int))
    access_token = create_access_token(
        data={"username": user.username, "role": user.role.value},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
