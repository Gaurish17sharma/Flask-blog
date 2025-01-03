"""added foreign key and one to many relationship for posts and users

Revision ID: f1096619de95
Revises: 4c2acd2bfe43
Create Date: 2025-01-01 13:12:41.587053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1096619de95'
down_revision = '4c2acd2bfe43'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('users_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'users', ['users_id'], ['id'])
        batch_op.drop_column('author')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('users_id')

    # ### end Alembic commands ###
