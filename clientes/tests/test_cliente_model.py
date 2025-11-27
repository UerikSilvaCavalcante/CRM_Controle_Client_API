"""

Testes do modelo de clientes
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from clientes.models import Clientes


@pytest.mark.parametrize(
    "cliente, expected",
    [
        # Teste para um cliente válido
        (
            # Entrada
            {
                "name": "Teste",
                "email": "Teste@example.com",
                "phone": "1234567890",
            },
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
            {
                "name": "Teste",
                "email": "",
                "phone": "",
            },
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
    cliente = Clientes(**cliente)
    assert expected["name"] == cliente.name
    assert expected["email"] == cliente.email
    assert expected["phone"] == cliente.phone


@pytest.mark.parametrize(
    "entrada",
    [123, "123", None, "", [], {}, {"name": None, "email": None, "phone": None}],
)
def test_cliente_model_invalido(entrada):
    """
    Testa o modelo do cliente com entradas invalidas
    """
    with pytest.raises((TypeError, ValidationError)):
        clientes = Clientes(**entrada)
        clientes.full_clean()


class TestClienteEmail(TestCase):
    """
    Testa criar um cliente com email duplicado
    """

    def setUp(self) -> None:
        """
        Configurações iniciais
        """
        self.cliente = Clientes.objects.create(
            name="Teste",
            email="Teste@example.com",
            phone="1234567890",
        )

    def setDown(self):
        """
        Exclui o cliente
        """
        self.cliente.delete()

    def test_email_unique(self):
        """
        Testa criar um cliente com email duplicado
        """
        with self.assertRaises(Exception):
            Clientes.objects.create(
                name="Teste",
                email="Teste@example.com",
                phone="1234567890",
            )
