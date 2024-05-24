from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.cliente.schemas import ClientCreate, ClientResponse
from api.cliente.services import ClientService
from api.cliente.repositories import ClientDatabaseRepository
from api.infra.db import get_db

client_router = APIRouter()


@client_router.post("/clients", response_model=ClientResponse)
def register_client(client: ClientCreate, db: Session = Depends(get_db)):
    client_repository = ClientDatabaseRepository(db)
    client_service = ClientService(client_repository)
    try:
        new_client = client_service.create_client(client)
        return new_client
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
