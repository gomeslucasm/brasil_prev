from datetime import datetime
from sqlalchemy.orm import Session
from api.cliente.models import Client
from api.plano.repositories import IPlanoRepository, PlanoDatabaseRepository
from api.produto.models import Produto
from api.produto.repositories import IProdutoRepository, ProdutoDatabaseRepository
from api.cliente.repositories import ClientDatabaseRepository, IClientRepository
from api.plano.schemas import PlanoCreate
from api.plano.models import Plano
from api.plano.entities import ProdutoData


class PlanoService:
    def __init__(
        self,
        plano_repository: IPlanoRepository,
        produto_repository: IProdutoRepository,
        cliente_repository: IClientRepository,
    ):
        self.plano_repository = plano_repository
        self.produto_repository = produto_repository
        self.cliente_repository = cliente_repository

    def validate_plano(
        self, *, produto: Produto, cliente: Client, plano: PlanoCreate
    ) -> ProdutoData:
        if produto.expiracao_de_venda < plano.data_da_contratacao:
            raise Exception(
                "Não é possível contratar um produto com prazo de venda expirado."
            )

        if plano.aporte < produto.valor_minimo_aporte_inicial:
            raise Exception("O valor do aporte é menor que o valor mínimo permitido.")

        if cliente.data_de_nascimento:
            idade_cliente = (
                plano.data_da_contratacao - cliente.data_de_nascimento
            ).days // 365
        else:
            raise Exception("Data de nascimento do cliente não encontrada.")

        if idade_cliente < produto.idade_de_entrada:
            raise Exception("O cliente não atende à idade mínima de entrada.")

        if plano.idade_de_aposentadoria > produto.idade_de_saida:
            raise Exception(
                "A idade de aposentadoria é maior que a idade máxima de saída."
            )

        produto_data = ProdutoData(
            id_produto=plano.id_produto,
            nome=produto.nome,
            susep=produto.susep,
            expiracao_de_venda=produto.expiracao_de_venda,
            valor_minimo_aporte_inicial=produto.valor_minimo_aporte_inicial,
            valor_minimo_aporte_extra=produto.valor_minimo_aporte_extra,
            idade_de_entrada=produto.idade_de_entrada,
            idade_de_saida=produto.idade_de_saida,
            carencia_inicial_de_resgate=produto.carencia_inicial_de_resgate,
            carencia_entre_resgates=produto.carencia_entre_resgates,
        )

        return produto_data

    def create_plano(self, plano: PlanoCreate) -> Plano:
        cliente = self.cliente_repository.get_by_id(plano.id_cliente)

        if not cliente:
            raise Exception("Cliente não encontrado.")

        produto = self.produto_repository.get_by_id(plano.id_produto)

        if not produto:
            raise Exception("Produto não encontrado.")

        produto_data = self.validate_plano(
            cliente=cliente, produto=produto, plano=plano
        )

        new_plano = self.plano_repository.create(
            id_cliente=plano.id_cliente,
            aporte=plano.aporte,
            data_da_contratacao=plano.data_da_contratacao,
            idade_de_aposentadoria=plano.idade_de_aposentadoria,
            produto_data=produto_data,
        )
        return new_plano


def create_plano_service(db: Session) -> PlanoService:
    plano_repository = PlanoDatabaseRepository(db)
    produto_repository = ProdutoDatabaseRepository(db)
    cliente_repository = ClientDatabaseRepository(db)
    plano_service = PlanoService(
        plano_repository, produto_repository, cliente_repository
    )
    return plano_service
