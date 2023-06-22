from sqlalchemy.orm import Session
from app.models.users import User

# Purpose: CRUD operations for users

async def get_user_by_email(db: Session, email: str) -> (User | None):
    return db.query(User).filter(User.email == email).first()

