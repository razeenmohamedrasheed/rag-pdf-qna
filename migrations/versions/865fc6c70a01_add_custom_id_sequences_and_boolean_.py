
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "865fc6c70a01"
down_revision: Union[str, Sequence[str], None] = "d9bb62e8740a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create PostgreSQL sequences
    op.execute("CREATE SEQUENCE role_id_seq START WITH 1")
    op.execute("CREATE SEQUENCE pdf_user_id_seq START WITH 1")

    # Assign sequences to primary key columns
    op.execute("ALTER SEQUENCE role_id_seq OWNED BY roles.id")
    op.execute("ALTER SEQUENCE pdf_user_id_seq OWNED BY users.id")

    # Set automatic ID generation
    op.alter_column(
        "roles",
        "id",
        server_default=sa.text("'role_' || nextval('role_id_seq')::text")
    )

    op.alter_column(
        "users",
        "id",
        server_default=sa.text("'pdf_user_' || nextval('pdf_user_id_seq')::text")
    )

    # Restore missing is_active column
    op.add_column(
        "users",
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False
        )
    )

    # Set database-side default for is_verified
    op.alter_column(
        "users",
        "is_verified",
        server_default=sa.text("false")
    )


def downgrade() -> None:
    # Remove automatic ID defaults
    op.alter_column("users", "id", server_default=None)
    op.alter_column("roles", "id", server_default=None)

    # Remove Boolean default
    op.alter_column("users", "is_verified", server_default=None)

    # Remove restored column
    op.drop_column("users", "is_active")

    # Remove sequences
    op.execute("DROP SEQUENCE pdf_user_id_seq")
    op.execute("DROP SEQUENCE role_id_seq")
