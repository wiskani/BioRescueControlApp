from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, create_token, authenticate_user
from app.schemas.users import Users

router: APIRouter = APIRouter()

#Create token
@router.post(
    path="/token",
    status_code=status.HTTP_200_OK,
    summary="Create token",
    tags=["Auth"],
)
async def generate_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> dict[str, str]:
    user  = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o password incorrecto"
        )
    return await create_token(user)

