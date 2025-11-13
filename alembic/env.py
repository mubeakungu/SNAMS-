from app.database import Base, SQLALCHEMY_DATABASE_URL
# Import all models so Alembic can discover them
from app.models import user, device # noqa
