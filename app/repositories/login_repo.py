import logging

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.users import User

logger = logging.getLogger(__name__)

class LoginRepository:
    def __init__(self, db:Session):
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