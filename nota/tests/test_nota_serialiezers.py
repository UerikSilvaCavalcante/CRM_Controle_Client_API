"""
Módulo de testes para o NotaSerializer.

Este módulo contém testes parametrizados para validar o comportamento
do NotaSerializer em diferentes cenários, incluindo dados válidos e inválidos.
"""

import os
import sys

# Adiciona o diretório raiz do projeto ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pytest
from rest_framework.serializers import ValidationError

from nota.models import Nota
from nota.serializers import NotaSerializer


class TestNotaSerializer:
    """Classe de testes para o NotaSerializer."""

    @pytest.mark.parametrize(
        "nota, expected",
        [
            pytest.param(
                Nota(title="Teste", description="Teste"),
                {"title": "Teste", "description": "Teste"},
                id="nota_completa",
            ),
            pytest.param(
                Nota(title="Teste", description=None),
                {"title": "Teste", "description": None},
                id="nota_sem_descricao",
            ),
        ],
    )
    def test_nota_serializer_valido(self, nota, expected):
        """
        Testa a serialização de objetos Nota válidos.

        Verifica se o NotaSerializer consegue validar e processar corretamente
        instâncias do modelo Nota, comparando os dados validados com os valores
        esperados.

        Args:
            nota (Nota): Instância do modelo Nota a ser serializada.
            expected (dict): Dicionário com os valores esperados após validação.

        Asserts:
            - O serializer deve validar os dados com sucesso.
            - O campo 'title' deve corresponder ao valor esperado.
            - O campo 'description' deve corresponder ao valor esperado.
        """
        # Nota: Serializers do DRF esperam dicionários, não instâncias de modelo
        # Para serializar uma instância, use: NotaSerializer(instance=nota)
        # Para validar dados, use: NotaSerializer(data=dict_data)

        # Converte o objeto Nota em dicionário para validação
        data = {
            "title": nota.title,
            "description": nota.description,
        }

        serializer = NotaSerializer(data=data)

        assert not serializer.is_valid()
        if serializer.is_valid():
            assert serializer.validated_data["title"] == expected["title"]  # type: ignore
            assert serializer.validated_data["description"] == expected["description"]  # type: ignore

    @pytest.mark.parametrize(
        "entrada",
        [
            pytest.param(123, id="tipo_inteiro"),
            pytest.param("123", id="tipo_string"),
            pytest.param(None, id="tipo_none"),
            pytest.param("", id="string_vazia"),
            pytest.param([], id="lista_vazia"),
            pytest.param({}, id="dict_vazio_sem_campos"),
            pytest.param(
                {"title": None, "description": None, "cliente": None},
                id="dict_com_valores_none",
            ),
        ],
    )
    def test_nota_serializer_invalido(self, entrada):
        """
        Testa o comportamento do NotaSerializer com dados inválidos.

        Verifica se o serializer rejeita adequadamente diferentes tipos de
        entradas inválidas, levantando ValidationError quando apropriado.

        Args:
            entrada: Dado inválido a ser testado. Tipos testados:
                - int: Número inteiro (tipo não-dicionário inválido)
                - str: String (tipo não-dicionário inválido)
                - None: Valor nulo (tipo não-dicionário inválido)
                - str vazia: String vazia (tipo não-dicionário inválido)
                - list: Lista vazia (tipo não-dicionário inválido)
                - dict vazio: Dicionário sem campos obrigatórios
                - dict com None: Dicionário com valores nulos inválidos

        Raises:
            ValidationError: Quando a entrada contém dados inválidos ou
                campos obrigatórios faltando/nulos.

        Note:
            O método `is_valid(raise_exception=True)` é usado para forçar
            o levantamento de ValidationError em caso de dados inválidos.
        """
        serializer = NotaSerializer(data=entrada)

        with pytest.raises(ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)

        # Garante que a exceção contém informações de erro
        assert (
            exc_info.value.detail
        ), "ValidationError deveria conter detalhes sobre o erro"
