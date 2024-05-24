from typing_extensions import Annotated
from pydantic import BeforeValidator, AfterValidator

import re


def only_cpf_numbers(cpf: str) -> str:
    cpf = str(cpf)

    return re.sub(r"\D", "", cpf)


def validate_cpf(cpf: str) -> str:
    cpf = re.sub(r"\D", "", cpf)

    if len(cpf) != 11:
        raise ValueError("Invalid cpf")

    if cpf == cpf[0] * 11:
        raise ValueError("Invalid cpf")

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    primeiro_digito = (soma * 10 % 11) % 10
    if int(cpf[9]) != primeiro_digito:
        raise ValueError("Invalid cpf")

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    segundo_digito = (soma * 10 % 11) % 10
    if int(cpf[10]) != segundo_digito:
        raise ValueError("Invalid cpf")

    return cpf


CPFPydanticType = Annotated[
    str, BeforeValidator(only_cpf_numbers), AfterValidator(validate_cpf)
]
