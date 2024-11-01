"""Add total_questions to QuizResult

Revision ID: 7578dae75219
Revises: ae5e4b74da1e
Create Date: 2024-10-28 15:08:22.516231

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7578dae75219'
down_revision = 'ae5e4b74da1e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quiz_result', schema=None) as batch_op:
        batch_op.add_column(sa.Column('total_questions', sa.Integer(), nullable=False, server_default='0'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quiz_result', schema=None) as batch_op:
        batch_op.drop_column('total_questions')

    # ### end Alembic commands ###
