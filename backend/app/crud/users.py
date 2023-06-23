from sqlalchemy.orm import Session
from app.models.users import User
from app.schemas.users import UsersCreate

# Purpose: CRUD operations for users

#Get if user exists
async def get_first_user(db: Session) -> (User | None):
    return db.query(User).first()

# Get a user by email
async def get_user_by_email(db: Session, email: str) -> (User | None):
    return db.query(User).filter(User.email == email).first()

#Create a user
async def create_user(db: Session, user: UsersCreate) -> User:
    if get_user_by_email(db, user.email) is not None:
        raise Exception("User already exists")
    db_user: User = User(email=user.email, permissions=user.permissions, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
 

