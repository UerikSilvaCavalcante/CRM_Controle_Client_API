"""
Testes do endpoint de notas
"""

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status
import os
import sys
from services.redis_service import RedisService

# Configurar path do Django antes de importar modelos locais
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from nota.models import Nota
from clientes.models import Clientes


class NotaAPITestCase(APITestCase):
    """
    API test para as rotas de Nota
    """

    def setUp(self):
        """
        Configurações iniciais para realizar os testes de API
        """
        self.url = reverse("notas-list")
        self.client_auth = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="useremail3124@example.com",
        )
        self.group, created = Group.objects.get_or_create(name="Vendedor")

        permission_codenames = [
            f"add_{Nota._meta.model_name}",
            f"change_{Nota._meta.model_name}",
            f"delete_{Nota._meta.model_name}",
            f"view_{Nota._meta.model_name}",
        ]

        content_type = ContentType.objects.get_for_model(Nota)
        for codename in permission_codenames:
            try:
                permission = Permission.objects.get(
                    codename=codename,
                    content_type=content_type,
                )
                self.group.permissions.add(permission)
            except Permission.DoesNotExist:
                # Se não existir, cria (mas normalmente já existe)
                permission = Permission.objects.create(
                    name=codename.replace("_", " ").title(),
                    codename=codename,
                    content_type=content_type,
                )
                self.group.permissions.add(permission)

        self.user.groups.add(self.group)
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

    def tearDown(self):
        """
        Limpeza após cada teste
        """

        # Limpar dados do banco
        User.objects.all().delete()
        Group.objects.all().delete()
        Nota.objects.all().delete()
        Clientes.objects.all().delete()
        Token.objects.all().delete()

    def test_get_notas_user(self):
        """
        Teste para verificar se o usuário pode obter as notas
        """
        self.client_auth.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user}")
        self.client_auth.force_authenticate(user=self.user)
        response = self.client_auth.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # type: ignore

    def test_get_notas_superuser(self):
        """
        Teste para verificar se o super usuário pode obter as notas"""
        self.client_auth.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_super_user}"
        )
        self.client_auth.force_authenticate(user=self.super_user)
        response = self.client_auth.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # type: ignore

    def test_post_notas(self):
        """
        Teste para verificar se o usuário pode criar uma nota
        """
        self.client_auth.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user}")
        self.client_auth.force_authenticate(user=self.user)
        data = {
            "cliente": self.cliente.pk,
            "title": "Teste",
            "description": "Teste",
        }
        response = self.client_auth.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # type: ignore

    def test_post_notas_not_exits_cliente(self):
        """
        Teste para verificar se o usuário nao criar uma nota sem cliente
        """
        self.client_auth.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user}")
        self.client_auth.force_authenticate(user=self.user)
        data = {
            "title": "Teste",
            "description": "Teste",
            "cliente": 4,
        }
        response = self.client_auth.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # type: ignore

    def test_delete_notas(self):
        """
        Teste para verificar se o usuário pode deletar uma nota
        """
        self.client_auth.force_authenticate(user=self.user)
        nota = Nota.objects.create(
            cliente=self.cliente, title="Teste", description="Teste"
        )

        response = self.client_auth.delete(f"{self.url}{nota.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # type: ignore

    def test_put_notas(self):
        """
        Teste para verificar se o usuário pode atualizar uma nota
        """

        self.client_auth.force_authenticate(user=self.user)
        nota = Nota.objects.create(
            cliente=self.cliente, title="Teste", description="Teste"
        )
        data = {
            "title": "Teste",
            "description": "Teste",
            "cliente": self.cliente.pk,
        }
        response = self.client_auth.put(f"{self.url}{nota.pk}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # type: ignore
