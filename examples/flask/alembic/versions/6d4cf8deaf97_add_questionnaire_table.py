"""add questionnaire table

Revision ID: 6d4cf8deaf97
Revises: b7302f83d979
Create Date: 2016-12-25 22:14:24.378999

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d4cf8deaf97'
down_revision = 'b7302f83d979'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('apk', sa.String(length=255), nullable=True),
    sa.Column('owner', sa.String(length=20), nullable=True),
    sa.Column('question', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_question_apk'), 'question', ['apk'], unique=False)
    op.create_index(op.f('ix_question_id'), 'question', ['id'], unique=False)
    op.create_index(op.f('ix_question_owner'), 'question', ['owner'], unique=False)
    op.create_index(op.f('ix_question_question'), 'question', ['question'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_question_question'), table_name='question')
    op.drop_index(op.f('ix_question_owner'), table_name='question')
    op.drop_index(op.f('ix_question_id'), table_name='question')
    op.drop_index(op.f('ix_question_apk'), table_name='question')
    op.drop_table('question')
    # ### end Alembic commands ###