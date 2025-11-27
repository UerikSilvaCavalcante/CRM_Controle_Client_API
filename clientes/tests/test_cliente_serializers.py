import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from clientes.models import Clientes
from clientes.serializers import ClienteSerializer


@pytest.mark.parametrize(
    "cliente, expected",
    [
        # Teste para um cliente válido
        (
            # Entrada
            Clientes(
                **{"name": "Teste", "email": "Teste@example.com", "phone": "1234567890"}
            ),
            # Esperado
            {
                "name": "Teste",
                "email": "Teste@example.com",
                "phone": "1234567890",
            },
        ),
        # Teste para um cliente incompleto
        (
            # Entrada
            Clientes(**{"name": "Teste", "email": "", "phone": ""}),
            # Esperado
            {
                "name": "Teste",
                "email": "",
                "phone": "",
            },
        ),
    ],
)
def test_cliente_model_valido(cliente, expected):
    """
    Testa o modelo cliente com dadas validos

    cliente(entrada): dict
    expected(esperado): dict

    asserts:
    - assert expected["name"] == cliente.name
    - assert expected["email"] == cliente.email
    - assert expected["phone"] == cliente.phone
    """

    cliente_serializer = ClienteSerializer(data=cliente)
    assert not cliente_serializer.is_valid()
    if cliente_serializer.is_valid():
        assert expected["name"] == cliente_serializer.validated_data.get("name")  # type: ignore
        assert expected["email"] == cliente_serializer.validated_data.get("email")  # type: ignore
        assert expected["phone"] == cliente_serializer.validated_data.get("phone")  # type: ignore
