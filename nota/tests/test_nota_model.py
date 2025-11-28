"""
Testes do modelo de Nota
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from nota.models import Nota


@pytest.mark.parametrize(
    "nota, expected",
    [
        (
            {
                "title": "Teste",
                "description": "Teste",
            },
            {
                "title": "Teste",
                "description": "Teste",
            },
        ),
        (
            {
                "title": "Teste",
                "description": None,
            },
            {
                "title": "Teste",
                "description": None,
            },
        ),
    ],
)
def test_nota_model(nota, expected):
    """
    Teste para verificar se o modelo Nota funciona corretamente
    """
    nota = Nota(**nota)

    assert nota.title == expected["title"]
    assert nota.description == expected["description"]


@pytest.mark.parametrize(
    "entrada",
    [
        123,
        "123",
        None,
        "",
        [],
        {},
        {"title": None, "description": None, "cliente": None},
    ],
)
def test_nota_model_invalido(entrada):
    """
    Teste para verificar se o modelo Nota funciona corretamente
    """
    with pytest.raises((TypeError, ValidationError)):
        notas = Nota(**entrada)
        notas.full_clean()
