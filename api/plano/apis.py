from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.plano.schemas import PlanoCreate, PlanoResponse
from api.plano.services import create_plano_service
from api.infra.db import get_db

plano_router = APIRouter()


@plano_router.post("/planos", response_model=PlanoResponse)
def register_plano(plano: PlanoCreate, db: Session = Depends(get_db)):
    try:
        plano_service = create_plano_service(db)
        new_plano = plano_service.create_plano(plano)
        return new_plano
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
