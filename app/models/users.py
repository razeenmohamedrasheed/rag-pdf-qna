from sqlalchemy import Boolean, DateTime, ForeignKey, Sequence, String, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

user_id_seq = Sequence("pdf_user_id_seq", metadata=Base.metadata)

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(50), user_id_seq, primary_key=True, server_default=text("'pdf_user_' || nextval('pdf_user_id_seq')::text"))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role_id: Mapped[str] = mapped_column(String(50), ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=text("true"), nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("false"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    role: Mapped["Role"] = relationship("Role", back_populates="users")