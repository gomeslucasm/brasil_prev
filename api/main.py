from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.responses import PlainTextResponse

from api.common.errors import BaseError
from .infra.db import get_db
from api.cliente.apis import client_router
from api.produto.apis import produto_router
from api.plano.apis import plano_router
from sqlalchemy.sql import text

app = FastAPI()


def register_apis(app):
    app.include_router(client_router, prefix="/api")
    app.include_router(produto_router, prefix="/api")
    app.include_router(plano_router, prefix="/api")


def register_models():
    from api.cliente.models import Client
    from api.produto.models import Produto
    from api.plano.models import Plano, ProdutoPlano


def register_error_handlers(app):
    @app.exception_handler(Exception)
    async def handle_default_exception(request, exc):
        import logging

        logger = logging.getLogger(__name__)

        logger.error(request.url, str(exc))

        if isinstance(exc, BaseError):
            return PlainTextResponse(str(exc), status_code=400)

        return PlainTextResponse("Internal server error", status_code=500)


register_models()
register_apis(app)
register_error_handlers(app)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/test-db")
async def test_db(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1"))
        return {"status": "success", "result": result.scalar()}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
