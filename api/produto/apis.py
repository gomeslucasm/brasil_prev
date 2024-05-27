from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.produto.schemas import ProdutoCreate, ProdutoResponse
from api.produto.services import ProdutoService
from api.produto.repositories import ProdutoDatabaseRepository
from api.infra.db import get_db

produto_router = APIRouter()


@produto_router.post("/produtos", response_model=ProdutoResponse)
def register_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    """
    Registrar produto
    """
    produto_repository = ProdutoDatabaseRepository(db)
    produto_service = ProdutoService(produto_repository)
    new_produto = produto_service.create_produto(produto)
    return new_produto
