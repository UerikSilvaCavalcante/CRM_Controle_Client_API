import os
import sys

from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from auth_user.serializers import UserAuthSerializer


# Create your tests here.
class TestSerializerAuthUser:
    """
    Class de Teste para o Serializer

    Metodos:
    - test_valid_data -> Teste para verificar se o serializer aceita dados válidos
    - test_invalid_data -> Teste para verificar se o serializer rejeita dados inválidos
    """

    def test_valid_data(self):
        """
        Teste para verificar se o serializer aceita dados válidos
        """
        data = {"username": "user", "password": "password"}
        serializer = UserAuthSerializer(data=data)
        assert serializer.is_valid()

    @pytest.mark.parametrize(
        "entrada",
        [
            {"username": "", "password": "password"},
            {"username": "user", "password": ""},
            123,
            [],
            "Teste",
            {},
            {"username": None},
        ],
    )
    def test_invalid_data(self, entrada):
        """
        Teste para verificar se o serializer rejeita dados inválidos
        """

        serializer = UserAuthSerializer(data=entrada)

        with pytest.raises(ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)

        # Garante que a exceção contém informações de erro
        assert (
            exc_info.value.detail  # type: ignore
        ), "ValidationError deveria conter detalhes sobre o erro"


class TestAPITestCaseAuthUser(APITestCase):
    """
    Class de Teste para o APITestCase

    metodos:
        - setUp -> Configurações iniciais para realizar os testes de API


    """

    def setUp(self):
        self.url = reverse("login")
        self.client_auth = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="useremail3124@example.com",
        )
        self.super_user = User.objects.create_superuser(
            username="superuser",
            password="testpassword",
            email="superemail3124@example.com",
        )
        Token.objects.get_or_create(user=self.user)
        Token.objects.get_or_create(user=self.super_user)
        self.token_user = Token.objects.get(user=self.user).key
        self.token_super_user = Token.objects.get(user=self.super_user).key

    def test_login(self):
        """
        Teste para verificar se o login funciona corretamente
        """
        response = self.client_auth.post(
            self.url,
            {"username": "testuser", "password": "testpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # type: ignore

    def test_login_superuser(self):
        """
        Teste para verificar se o login do super usuário funciona corretamente
        """
        response = self.client_auth.post(
            self.url,
            {"username": "superuser", "password": "testpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # type: ignore

    def test_login_invalid_credentials(self):
        """
        Teste para verificar se o login rejeita credenciais inválidas
        """
        response = self.client_auth.post(
            self.url,
            {"username": "invaliduser", "password": "invalidpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # type: ignore
