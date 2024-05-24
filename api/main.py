from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .infra.db import get_db
from api.cliente.apis import client_router
from sqlalchemy.sql import text

app = FastAPI()


def register_apis(app):
    app.include_router(client_router, prefix="/api")


def register_models():
    from api.cliente.models import Client


register_models()
register_apis(app)


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
