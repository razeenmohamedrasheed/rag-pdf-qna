import logging

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.models.users import User
from app.utils.password_utility import HashPassword
from app.repositories.authentication_repo import UserRepository
from app.schemas.authentication_schema import ( Registration, 
                                                RegistrationResponse, 
                                                RegistartionFailureResponse )



logger = logging.getLogger(__name__)

def register_new_user(db: Session, payload: Registration):

    user_repo = UserRepository(db)

    user_exists = user_repo.get_user_by_email(payload.email)

    if user_exists:
        logger.info("User already exists")

        return RegistartionFailureResponse(
            status="Failed",
            message="Email already exists"
        )

    password_hash = HashPassword().hash_password(payload.password)

    role = user_repo.get_role_by_name("user")

    if not role:
        logger.error("Default user role not found")

        return RegistartionFailureResponse(
            status="Failed",
            message="Default role not configured"
        )

    new_user = User(
        name=payload.name,
        email=payload.email,
        password_hash=password_hash,
        role_id=role.id
    )

    registered_user = user_repo.create_user(new_user)

    logger.info("User registered successfully")

    return RegistrationResponse(
        status="Success",
        user_id=registered_user.id,
        created_at=registered_user.created_at
    )
        
        
