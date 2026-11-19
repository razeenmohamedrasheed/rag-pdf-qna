import logging

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.users import User
from app.models.roles import Role

logger = logging.getLogger(__name__)


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str):

        try:
            statement = select(User).where(
                User.email == email
            )

            return self.db.execute(
                statement
            ).scalar_one_or_none()

        except SQLAlchemyError:
            logger.exception("Failed to fetch user by email")
            raise

    def create_user(self, user: User):

        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)

            return user

        except SQLAlchemyError:
            self.db.rollback()
            logger.exception("Failed to create user")
            raise

    def get_role_by_name(self, role_name: str):
        try:
            statement = select(Role).where(
                Role.name == role_name
            )

            return self.db.execute(statement).scalar_one_or_none()
        
        except SQLAlchemyError:
            logger.exception("Failed to fetch role")
            raise