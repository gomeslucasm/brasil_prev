from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session

from api.common.errors import NotFoundError, ValidationError
from api.common.utils import adjust_datetime_to_utc
from api.plano.repositories import IPlanoRepository, PlanoDatabaseRepository
from api.produto.repositories import IProdutoRepository, ProdutoDatabaseRepository
from api.cliente.repositories import ClientDatabaseRepository, IClientRepository
from api.plano.schemas import PlanoAporteExtra, PlanoCreate, Planoresgate
from api.plano.models import Plano, PlanoOperation
from api.produto.models import Produto
from api.cliente.models import Client
from api.plano.types import ProdutoData, PlanoData


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
        if adjust_datetime_to_utc(produto.expiracao_de_venda) < adjust_datetime_to_utc(
            plano.data_da_contratacao
        ):
            raise ValidationError(
                "Não é possível contratar um produto com prazo de venda expirado."
            )
        if plano.aporte < produto.valor_minimo_aporte_inicial:
            raise ValidationError(
                "O valor do aporte é menor que o valor mínimo permitido."
            )
        idade_cliente = (
            adjust_datetime_to_utc(plano.data_da_contratacao)
            - adjust_datetime_to_utc(cliente.data_de_nascimento)
        ).days // 365
        if idade_cliente < produto.idade_de_entrada:
            raise ValidationError("O cliente não atende à idade mínima de entrada.")
        if plano.idade_de_aposentadoria > produto.idade_de_saida:
            raise ValidationError(
                "A idade de aposentadoria é maior que a idade máxima de saída."
            )

        produto_data = ProdutoData(
            id_produto=produto.id,
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
        produto = self.produto_repository.get_by_id(plano.id_produto)
        if not produto:
            raise NotFoundError("Produto não encontrado.")
        cliente = self.cliente_repository.get_by_id(plano.id_cliente)
        if not cliente:
            raise NotFoundError("Cliente não encontrado.")
        produto_data = self.validate_plano(
            produto=produto, cliente=cliente, plano=plano
        )
        new_plano = self.plano_repository.create(
            id_cliente=plano.id_cliente,
            produto_data=produto_data,
            aporte=plano.aporte,
            data_da_contratacao=plano.data_da_contratacao,
            idade_de_aposentadoria=plano.idade_de_aposentadoria,
        )
        return new_plano

    def get_plano_data(self, id_plano: UUID):
        plano_data = self.plano_repository.get_plano_data(id_plano=id_plano)

        if not plano_data:
            raise NotFoundError("Plano not found")

        return plano_data

    def validate_aporte_extra(self, *, id_plano: UUID, value: float) -> bool:
        plano_data = self.get_plano_data(id_plano=id_plano)

        if value < plano_data.produto_valor_minimo_aporte_extra:
            raise ValidationError("O valor de aporte extra é menor que o permitido")

        return True

    def __carencia_inicial_de_resgate_is_valid(self, *, plano_data: PlanoData):
        print("plano_data.data_da_contratacao = ", plano_data.data_da_contratacao)
        return adjust_datetime_to_utc(datetime.now()) > (
            adjust_datetime_to_utc(plano_data.data_da_contratacao)
            + timedelta(days=plano_data.produto_carencia_inicial_de_resgate)
        )

    def __carencia_entre_resgates_is_valid(
        self, *, id_plano: UUID, plano_data: PlanoData
    ):
        last_resgate = self.plano_repository.get_last_resgate(id_plano=id_plano)

        if not last_resgate:
            return True

        return (
            adjust_datetime_to_utc(last_resgate.created_on)
            + timedelta(days=plano_data.produto_carencia_entre_resgates)
        ) < adjust_datetime_to_utc(datetime.now())

    def validate_resgate(self, *, id_plano: UUID, value: float) -> bool:
        plano_data = self.get_plano_data(id_plano=id_plano)

        if plano_data.aporte < value:
            raise ValidationError("O valor de aporte é menor que o de resgate")

        if not self.__carencia_inicial_de_resgate_is_valid(plano_data=plano_data):
            raise ValidationError(
                f"Ainda não é possível fazer resgatas devido ao tempo de carencia inicial de {plano_data.produto_carencia_inicial_de_resgate}"
            )

        if not self.__carencia_entre_resgates_is_valid(
            id_plano=id_plano, plano_data=plano_data
        ):
            raise ValidationError(
                f"Não é possível fazer o resgate por que o último resgate foi feito a menos de {plano_data.produto_carencia_entre_resgates} dias"
            )

        return True

    def aporte_extra(self, plano_aporte_extra: PlanoAporteExtra) -> PlanoOperation:
        return self.plano_repository.aporte_extra(
            id_plano=plano_aporte_extra.id_plano, value=plano_aporte_extra.value
        )

    def resgate(self, plano_resgate: Planoresgate):
        return self.plano_repository.resgate(
            id_plano=plano_resgate.id_plano, value=plano_resgate.value
        )


def create_plano_service(db: Session) -> PlanoService:
    plano_repository = PlanoDatabaseRepository(db)
    produto_repository = ProdutoDatabaseRepository(db)
    cliente_repository = ClientDatabaseRepository(db)
    plano_service = PlanoService(
        plano_repository, produto_repository, cliente_repository
    )
    return plano_service
