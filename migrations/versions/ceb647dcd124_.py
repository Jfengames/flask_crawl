"""empty message

Revision ID: ceb647dcd124
Revises: a0af907440af
Create Date: 2018-11-26 14:22:32.759744

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ceb647dcd124'
down_revision = 'a0af907440af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('commonparameters_tagged_new',
    sa.Column('dt', sa.String(length=50), nullable=True),
    sa.Column('province', sa.String(length=50), nullable=True),
    sa.Column('city', sa.String(length=50), nullable=True),
    sa.Column('region', sa.String(length=50), nullable=True),
    sa.Column('cgi', sa.String(length=50), nullable=False),
    sa.Column('tac', sa.Integer(), nullable=True),
    sa.Column('chinesename', sa.String(length=200), nullable=True),
    sa.Column('covertype', sa.String(length=50), nullable=True),
    sa.Column('scenario', sa.String(length=50), nullable=True),
    sa.Column('vendor', sa.String(length=50), nullable=True),
    sa.Column('earfcn', sa.Integer(), nullable=True),
    sa.Column('nettype', sa.String(length=50), nullable=True),
    sa.Column('pci', sa.Integer(), nullable=True),
    sa.Column('iscore', sa.Boolean(), nullable=True),
    sa.Column('gpslat', sa.Float(), nullable=True),
    sa.Column('gpslng', sa.Float(), nullable=True),
    sa.Column('bdlat', sa.Float(), nullable=True),
    sa.Column('bdlng', sa.Float(), nullable=True),
    sa.Column('angle', sa.Integer(), nullable=True),
    sa.Column('height', sa.String(length=50), nullable=True),
    sa.Column('totaltilt', sa.Float(), nullable=True),
    sa.Column('iscounty', sa.Boolean(), nullable=True),
    sa.Column('isauto', sa.Boolean(), nullable=True),
    sa.Column('flag', sa.Boolean(), nullable=True),
    sa.Column('residential_flag', sa.String(length=50), nullable=True),
    sa.Column('hospital_flag', sa.String(length=50), nullable=True),
    sa.Column('beauty_spot_flag', sa.String(length=50), nullable=True),
    sa.Column('college_flag', sa.String(length=50), nullable=True),
    sa.Column('food_centre_flag', sa.String(length=50), nullable=True),
    sa.Column('subway_flag', sa.String(length=50), nullable=True),
    sa.Column('high_speed_flag', sa.String(length=50), nullable=True),
    sa.Column('high_speed_rail_flag', sa.String(length=50), nullable=True),
    sa.Column('viaduct_flag', sa.String(length=50), nullable=True),
    sa.Column('high_rise_flag', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('cgi')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('commonparameters_tagged_new')
    # ### end Alembic commands ###
