from api.cliente.repositories import IClientRepository
from api.cliente.schemas import ClientCreate


class ClientService:
    def __init__(self, client_repository: IClientRepository):
        self.client_repository = client_repository

    def create_client(self, client: ClientCreate):
        db_client = self.client_repository.get_by_cpf(client.cpf)
        if db_client:
            raise Exception(f"Client with this CPF={client.cpf} already exists.")

        new_client = self.client_repository.create(
            cpf=client.cpf,
            nome=client.nome,
            email=client.email,
            dataDeNascimento=client.dataDeNascimento,
            genero=client.genero,
            rendaMensal=client.rendaMensal,
        )
        return new_client
