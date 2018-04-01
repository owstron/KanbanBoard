"""empty message

Revision ID: 31c8942c42b4
Revises: 
Create Date: 2018-04-01 22:25:46.409934

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31c8942c42b4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstName', sa.String(), nullable=True),
    sa.Column('lastName', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('passwordHash', sa.String(), nullable=True),
    sa.Column('passwordSalt', sa.String(), nullable=True),
    sa.Column('maxProgressLimit', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('tasks',
    sa.Column('taskId', sa.Integer(), nullable=False),
    sa.Column('taskName', sa.String(), nullable=True),
    sa.Column('taskDesc', sa.String(), nullable=True),
    sa.Column('taskStatus', sa.String(), nullable=True),
    sa.Column('userId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ),
    sa.PrimaryKeyConstraint('taskId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks')
    op.drop_table('users')
    # ### end Alembic commands ###