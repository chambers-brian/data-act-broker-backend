"""renameErrorsPresent

Revision ID: 6ab05a4cee27
Revises: a17156edb8a0
Create Date: 2016-04-08 12:23:13.440000

"""

# revision identifiers, used by Alembic.
revision = '6ab05a4cee27'
down_revision = 'a17156edb8a0'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_error_data():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('file_status', sa.Column('row_errors_present', sa.Boolean(), nullable=True))
    op.drop_column('file_status', 'errors_present')
    ### end Alembic commands ###


def downgrade_error_data():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('file_status', sa.Column('errors_present', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('file_status', 'row_errors_present')
    ### end Alembic commands ###


def upgrade_job_tracker():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_job_tracker():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_user_manager():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_user_manager():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###

