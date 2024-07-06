"""Add Table

Revision ID: 704c7b3c0a7d
Revises: 3b29f47f4a50
Create Date: 2024-06-29 15:21:13.954657

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '704c7b3c0a7d'
down_revision: Union[str, None] = '3b29f47f4a50'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vacancies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('site_id', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('company', sa.String(), nullable=False),
    sa.Column('area', sa.String(), nullable=False),
    sa.Column('experience', sa.String(), nullable=False),
    sa.Column('schedule', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('salary_from', sa.Integer(), nullable=True),
    sa.Column('salary_to', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('site_id')
    )
    op.create_index(op.f('ix_vacancies_id'), 'vacancies', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_vacancies_id'), table_name='vacancies')
    op.drop_table('vacancies')
    # ### end Alembic commands ###