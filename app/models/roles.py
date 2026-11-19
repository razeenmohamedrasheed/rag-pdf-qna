from sqlalchemy import DateTime, Sequence, String, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

role_id_seq = Sequence("role_id_seq", metadata=Base.metadata)

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[str] = mapped_column(String(50), role_id_seq, primary_key=True, server_default=text("'role_' || nextval('role_id_seq')::text"))
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    users: Mapped[list["User"]] = relationship("User", back_populates="role")