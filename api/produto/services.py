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
            expiracao_de_venda=produto.expiracao_de_venda,
            valor_minimo_aporte_inicial=produto.valor_minimo_aporte_inicial,
            valor_minimo_aporte_extra=produto.valor_minimo_aporte_extra,
            idade_de_entrada=produto.idade_de_entrada,
            idade_de_saida=produto.idade_de_saida,
            carencia_inicial_de_resgate=produto.carencia_inicial_de_resgate,
            carencia_entre_resgates=produto.carencia_entre_resgates,
        )
        return new_produto
