from api.produto.repositories import IProdutoRepository
from api.produto.schemas import ProdutoCreate
from api.produto.models import Produto


class ProdutoService:
    def __init__(self, produto_repository: IProdutoRepository):
        self.produto_repository = produto_repository

    def create_produto(self, produto: ProdutoCreate) -> Produto:
        new_produto = self.produto_repository.create(
            nome=produto.nome,
            susep=produto.susep,
            expiracaoDeVenda=produto.expiracaoDeVenda,
            valorMinimoAporteInicial=produto.valorMinimoAporteInicial,
            valorMinimoAporteExtra=produto.valorMinimoAporteExtra,
            idadeDeEntrada=produto.idadeDeEntrada,
            idadeDeSaida=produto.idadeDeSaida,
            carenciaInicialDeResgate=produto.carenciaInicialDeResgate,
            carenciaEntreResgates=produto.carenciaEntreResgates,
        )
        return new_produto
