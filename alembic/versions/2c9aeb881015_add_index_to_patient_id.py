"""add index to patient_id

Revision ID: 2c9aeb881015
Revises: cdcd0f093a2f
Create Date: 2026-02-12 23:23:21.714015

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c9aeb881015'
down_revision: Union[str, Sequence[str], None] = 'cdcd0f093a2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "ix_encounters_patient_id",
        "clinical_encounters",
        ["patient_id"],
        unique=False
    )


def downgrade() -> None:
    op.drop_index(
        "ix_encounters_patient_id",
        table_name="clinical_encounters"
    )