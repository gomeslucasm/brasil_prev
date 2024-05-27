from api.cliente.repositories import IClientRepository
from api.cliente.schemas import ClientCreate
from api.common.errors import ValidationError


class ClientService:
    def __init__(self, client_repository: IClientRepository):
        self.client_repository = client_repository

    def create_client(self, client: ClientCreate):
        db_client = self.client_repository.get_by_cpf(client.cpf)
        if db_client:
            raise ValidationError(f"Client with this CPF={client.cpf} already exists.")

        new_client = self.client_repository.create(
            cpf=client.cpf,
            nome=client.nome,
            email=client.email,
            data_de_nascimento=client.data_de_nascimento,
            genero=client.genero,
            renda_mensal=client.renda_mensal,
        )
        return new_client
