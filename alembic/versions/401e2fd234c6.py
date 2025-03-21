"""init

Revision ID: 47f51a79482b
Revises: 
Create Date: 2025-03-18 19:37:59.647977

"""
from typing import Sequence, Union

import geoalchemy2
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47f51a79482b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['activities.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('buildings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city', sa.String(length=100), nullable=True),
    sa.Column('street', sa.String(length=255), nullable=True),
    sa.Column('house_number', sa.String(length=20), nullable=True),
    sa.Column('number_premises', sa.String(length=20), nullable=True),
    sa.Column('location', geoalchemy2.types.Geography(geometry_type='POINT', srid=4326, from_text='ST_GeogFromText', name='geography'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_buildings_location1', 'buildings', ['location'], unique=False, postgresql_using='gist')
    op.create_table('organizations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('building_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['building_id'], ['buildings.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organization_activity',
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.Column('activity_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['activity_id'], ['activities.id'], ),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], )
    )
    op.create_table('phone_numbers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.String(length=30), nullable=True),
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('spatial_ref_sys',
    sa.Column('srid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('auth_name', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('auth_srid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('srtext', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.Column('proj4text', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.CheckConstraint('srid > 0 AND srid <= 998999', name='spatial_ref_sys_srid_check'),
    sa.PrimaryKeyConstraint('srid', name='spatial_ref_sys_pkey')
    )
    op.drop_table('phone_numbers')
    op.drop_table('organization_activity')
    op.drop_table('organizations')
    op.drop_index('idx_buildings_location', table_name='buildings', postgresql_using='gist')
    op.drop_table('buildings')
    op.drop_table('activities')
    # ### end Alembic commands ###
