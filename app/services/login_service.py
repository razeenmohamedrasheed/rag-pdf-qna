import logging

from datetime import datetime
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException

from app.utils.password_utility import HashPassword
from app.repositories.login_repo import LoginRepository
from app.core.security import create_access_token,create_refresh_token
from app.schemas.login_schema import (
                                LoginPayload,
                                LoginFailureResponse,
                                LoginResponse
                                )

logger = logging.getLogger(__name__)

def user_login(payload:LoginPayload,db:Session):
    try:
        login_repo = LoginRepository(db)
        user = login_repo.get_user_by_email(payload.email)

        if not user:
            logger.error("Invalid credentials")
            return LoginFailureResponse(
                status="Failed",
                message="Invalid credentials"
            )
        password_verify = HashPassword().verify_password(payload.password,user.password_hash)

        if not password_verify:
            logger.error("Invalid credentials")
            return LoginFailureResponse(
                status="Failed",
                message="Invalid credentials"
            )
        access_token = create_access_token(str(user.id), user.email)
        refresh_token = create_refresh_token(str(user.id), user.email)
        
        return LoginResponse(
            status="success",
            message="Login Success",
            access_token=access_token,
            refresh_token=refresh_token,
            created_at = datetime.now()
        )
        

    except Exception as e:
        logger.exception("Login failed")
        raise HTTPException(500, f"{e}")