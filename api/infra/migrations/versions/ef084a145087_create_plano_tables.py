"""create plano tables

Revision ID: ef084a145087
Revises: c51550fb5cf1
Create Date: 2024-05-27 01:14:32.670841

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef084a145087'
down_revision: Union[str, None] = 'c51550fb5cf1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('produto_planos',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('id_produto', sa.UUID(), nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('susep', sa.String(), nullable=False),
    sa.Column('expiracao_de_venda', sa.DateTime(), nullable=False),
    sa.Column('valor_minimo_aporte_inicial', sa.Float(), nullable=False),
    sa.Column('valor_minimo_aporte_extra', sa.Float(), nullable=False),
    sa.Column('idade_de_entrada', sa.Integer(), nullable=False),
    sa.Column('idade_de_saida', sa.Integer(), nullable=False),
    sa.Column('carencia_inicial_de_resgate', sa.Integer(), nullable=False),
    sa.Column('carencia_entre_resgates', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_on', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('deleted_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planos',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('id_cliente', sa.UUID(), nullable=False),
    sa.Column('id_produto_plano', sa.UUID(), nullable=False),
    sa.Column('aporte', sa.Float(), nullable=False),
    sa.Column('data_da_contratacao', sa.DateTime(), nullable=False),
    sa.Column('idade_de_aposentadoria', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_on', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('deleted_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['id_cliente'], ['clientes.id'], ),
    sa.ForeignKeyConstraint(['id_produto_plano'], ['produto_planos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('planos')
    op.drop_table('produto_planos')
    # ### end Alembic commands ###
