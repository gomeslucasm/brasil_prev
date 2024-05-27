from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.plano.schemas import (
    PlanoAporteExtra,
    PlanoCreate,
    PlanoOperationResponse,
    PlanoResponse,
    PlanoRetirada,
)
from api.plano.services import create_plano_service
from api.infra.db import get_db

plano_router = APIRouter()


@plano_router.post("/planos", response_model=PlanoResponse)
def register_plano(plano: PlanoCreate, db: Session = Depends(get_db)):
    plano_service = create_plano_service(db)
    new_plano = plano_service.create_plano(plano)
    return new_plano


@plano_router.post("/planos/aporte", response_model=PlanoOperationResponse)
def aporte_extra_plano(
    plano_aporte_extra: PlanoAporteExtra, db: Session = Depends(get_db)
):
    plano_service = create_plano_service(db)
    plano_service.validate_aporte_extra(
        id_plano=plano_aporte_extra.id_plano, value=plano_aporte_extra.value
    )
    return plano_service.aporte_extra(plano_aporte_extra)


@plano_router.post("/planos/retirada", response_model=PlanoOperationResponse)
def retirada_plano(plano_retirada: PlanoRetirada, db: Session = Depends(get_db)):
    plano_service = create_plano_service(db)
    plano_service.validate_retirada(
        id_plano=plano_retirada.id_plano, value=plano_retirada.value
    )
    return plano_service.retirada(plano_retirada)
