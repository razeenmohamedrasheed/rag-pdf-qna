from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.login_service import user_login
from app.schemas.login_schema import (
                LoginPayload,
                LoginFailureResponse
)

router = APIRouter()


@router.post("/login")
def login(payload: LoginPayload, db: Session = Depends(get_db)):
    result = user_login(payload, db)
    
    if isinstance(result, LoginFailureResponse):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=result.model_dump()
        )
    
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=result.model_dump(mode="json")
    )

