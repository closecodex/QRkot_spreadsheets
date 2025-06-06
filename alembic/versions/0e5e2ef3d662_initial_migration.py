"""Initial migration

Revision ID: 0e5e2ef3d662
Revises: 
Create Date: 2025-01-22 23:58:55.734081

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e5e2ef3d662'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('charityproject',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_amount', sa.Integer(), nullable=False),
    sa.Column('fully_invested', sa.Boolean(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('close_date', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('invested_amount', sa.Integer(), nullable=True),
    sa.CheckConstraint('0 <= invested_amount <= full_amount', name='check_invested_amount_range'),
    sa.CheckConstraint('full_amount > 0', name='check_full_amount_positive'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('charityproject', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_charityproject_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_charityproject_name'), ['name'], unique=True)

    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_id'), ['id'], unique=False)

    op.create_table('donation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_amount', sa.Integer(), nullable=False),
    sa.Column('invested_amount', sa.Integer(), nullable=False),
    sa.Column('fully_invested', sa.Boolean(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('close_date', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('comment', sa.String(), nullable=True),
    sa.CheckConstraint('0 <= invested_amount <= full_amount', name='check_invested_amount_range'),
    sa.CheckConstraint('full_amount > 0', name='check_full_amount_positive'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('donation', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_donation_id'), ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('donation', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_donation_id'))

    op.drop_table('donation')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_id'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    with op.batch_alter_table('charityproject', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_charityproject_name'))
        batch_op.drop_index(batch_op.f('ix_charityproject_id'))

    op.drop_table('charityproject')
    # ### end Alembic commands ###
