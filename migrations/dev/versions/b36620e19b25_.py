"""empty message

Revision ID: b36620e19b25
Revises: 
Create Date: 2020-08-04 23:30:34.841600

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'b36620e19b25'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('participant_status',
    sa.Column('ctime', sa.BigInteger(), nullable=True),
    sa.Column('mtime', sa.BigInteger(), nullable=True),
    sa.Column('name', sa.Enum('pending', 'active', 'inactive', name='participantstatusenum'), nullable=False),
    sa.PrimaryKeyConstraint('name'),
    sa.UniqueConstraint('name')
    )
    op.create_table('wager_status',
    sa.Column('ctime', sa.BigInteger(), nullable=True),
    sa.Column('mtime', sa.BigInteger(), nullable=True),
    sa.Column('name', sa.Enum('pending', 'active', 'inactive', name='wagerstatusenum'), nullable=False),
    sa.PrimaryKeyConstraint('name'),
    sa.UniqueConstraint('name')
    )
    op.create_table('wager',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('ctime', sa.BigInteger(), nullable=True),
    sa.Column('mtime', sa.BigInteger(), nullable=True),
    sa.Column('owner_uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('status', sa.Enum('pending', 'active', 'inactive', name='wagerstatusenum'), nullable=True),
    sa.ForeignKeyConstraint(['status'], ['wager_status.name'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('contest',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('ctime', sa.BigInteger(), nullable=True),
    sa.Column('mtime', sa.BigInteger(), nullable=True),
    sa.Column('contest_uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('wager_uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.ForeignKeyConstraint(['wager_uuid'], ['wager.uuid'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('party',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('ctime', sa.BigInteger(), nullable=True),
    sa.Column('mtime', sa.BigInteger(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('wager_uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.ForeignKeyConstraint(['wager_uuid'], ['wager.uuid'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('participant',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('ctime', sa.BigInteger(), nullable=True),
    sa.Column('mtime', sa.BigInteger(), nullable=True),
    sa.Column('user_uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('party_uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('status', sa.Enum('pending', 'active', 'inactive', name='participantstatusenum'), nullable=False),
    sa.ForeignKeyConstraint(['party_uuid'], ['party.uuid'], ),
    sa.ForeignKeyConstraint(['status'], ['participant_status.name'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('stake',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('ctime', sa.BigInteger(), nullable=True),
    sa.Column('mtime', sa.BigInteger(), nullable=True),
    sa.Column('currency', sqlalchemy_utils.types.currency.CurrencyType(length=3), nullable=True),
    sa.Column('amount', sa.String(), nullable=True),
    sa.Column('participant_uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.ForeignKeyConstraint(['participant_uuid'], ['participant.uuid'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stake')
    op.drop_table('participant')
    op.drop_table('party')
    op.drop_table('contest')
    op.drop_table('wager')
    op.drop_table('wager_status')
    op.drop_table('participant_status')
    # ### end Alembic commands ###