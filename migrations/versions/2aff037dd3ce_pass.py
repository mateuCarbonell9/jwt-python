"""add password_hash column to user table

Revision ID: 2aff037dd3ce
Revises:
Create Date: 2025-03-19 09:58:35.741771
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "2aff037dd3ce"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Añadir la columna password_hash a la tabla 'user'
    op.add_column(
        "user", sa.Column("password_hash", sa.String(length=120), nullable=False)
    )

    # Si es necesario, agregar un índice en la nueva columna de password_hash
    # op.create_index('ix_user_password_hash', 'user', ['password_hash'])


def downgrade():
    # Eliminar la columna password_hash en caso de que se revierta la migración
    op.drop_column("user", "password_hash")
