from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.authentication_service import register_new_user
from app.schemas.authentication_schema import Registration, RegistrationResponse, RegistartionFailureResponse


router = APIRouter()


@router.post("/signup")
def register_user(payload: Registration, db: Session = Depends(get_db)):

    result = register_new_user(db, payload)

    if isinstance(result, RegistartionFailureResponse):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=result.model_dump()
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=result.model_dump(mode="json")
    )

