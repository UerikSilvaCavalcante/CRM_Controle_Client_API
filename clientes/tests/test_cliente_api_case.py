# pylint: disable=too-many-instance-attributes
"""
Testes do endpoint de clientes
"""
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status
import os
import sys

# Configurar path do Django antes de importar modelos locais
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from nota.models import Nota
from clientes.models import Clientes




class ClientesAPITestCase(APITestCase):
    """Testes do endpoint de clientes"""

    def setUp(self):
        """
        Configurações iniciais para realizar os testes de API

        """
        self.url = reverse("clientes-list")
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
        self.cliente = Clientes.objects.create(
            name="Teste",
            email="Teste@example.com",
            phone="1234567890",
            responsavel=self.user,
        )
        self.nota = Nota.objects.create(
            title="Teste",
            description="Teste",
            cliente=self.cliente,
        )

    def test_get_clientes_user(self):
        """
        Teste para verificar se o usuário pode obter os clientes
        """
        self.client_auth.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user}")
        self.client_auth.force_authenticate(user=self.user)
        response = self.client_auth.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # type: ignore

    def test_get_clientes_superuser(self):
        """
        Teste para verificar se o super usuário pode obter os clientes (todos)
        """
        self.client_auth.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_super_user}"
        )
        self.client_auth.force_authenticate(user=self.super_user)
        response = self.client_auth.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # type: ignore
        self.assertGreater(len(response.data), 0)  # type: ignore

    def test_get_clientes_not_auth(self):
        """
        Testa se um usuário não autenticado não pode obter os clientes
        """
        response = self.client_auth.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # type: ignore

    def test_post_clientes(self):
        """
        Teste para verificar se o usuário pode criar um cliente
        """
        self.client_auth.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user}")
        self.client_auth.force_authenticate(user=self.user)
        data = {"name": "Teste", "email": "teste2@example.com", "phone": "1234567890"}
        response = self.client_auth.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # type: ignore

    def test_post_invalid_email_unique_clientes(self):
        """
        Teste para verificar se o usuário não criar um cliente com email duplicado
        """
        self.client_auth.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user}")
        self.client_auth.force_authenticate(user=self.user)
        data = {
            "name": "Teste",
            "email": "Teste@example.com",
            "phone": "1234567890",
            "responsavel": self.user.pk,
        }
        response = self.client_auth.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # type: ignore

    def test_post_invalid_email_clientes(self):
        """
        Teste para verificar se o usuário nao criar um cliente com email invalido
        """
        self.client_auth.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user}")
        self.client_auth.force_authenticate(user=self.user)
        data = {
            "name": "Teste",
            "email": "Testeexample.com",
            "phone": "1234567890",
            "responsavel": self.user.pk,
        }
        response = self.client_auth.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # type: ignore

    def test_post_invalid_clientes(self):
        """
        Teste para verificar se o usuário nao criar um cliente invalido
        """
        self.client_auth.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user}")
        self.client_auth.force_authenticate(user=self.user)
        data = {
            "email": "teste2@example.com",
            "phone": "1234567890",
            "responsavel": self.user.pk,
        }
        response = self.client_auth.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # type: ignore

    def test_post_cliente_invalid_user(self):
        """
        Teste para verificar se o usuário nao criar um cliente com usuário invalido
        """
        self.client_auth.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user}")
        self.client_auth.force_authenticate(user=self.user)
        data = {
            "name": "Teste",
            "email": "teste2@example.com",
            "phone": "1234567890",
            "responsavel": 4,
        }
        response = self.client_auth.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # type: ignore
