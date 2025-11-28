from clientes.models import Clientes
from django.contrib.auth.models import User
from nota.models import Nota


def create_user():
    user = User.objects.create_user(
        username="testuser",
        password="testpassword",
        email="useremail3124@example.com",
    )
    return user


def populate_database_clientes():
    clientes = (
        {
            "name": "João",
            "email": "jE0k4@example.com",
            "phone": "1234567890",
            "responsavel": 1,
        },
        {
            "name": "Pedro",
            "email": "pE3k4@example.com",
            "phone": "9876543210",
            "responsavel": 1,
        },
        {
            "name": "Ana",
            "email": "aE2k4@example.com",
            "phone": "5555555555",
            "responsavel": 1,
        },
        {
            "name": "Maria",
            "email": "1e2dI@example.com",
            "phone": "1234567890",
            "responsavel": 1,
        },
    )
    for cliente in clientes:
        Clientes.objects.create(**cliente)


def pupulate_database_notas():
    notas = (
        {"title": "Nota 1", "description": "Descrição da nota 1", "cliente": 1},
        {"title": "Nota 2", "description": "Descrição da nota 2", "cliente": 1},
        {"title": "Nota 3", "description": "Descrição da nota 3", "cliente": 2},
        {"title": "Nota 4", "description": "Descrição da nota 4", "cliente": 2},
    )
    for nota in notas:
        Nota.objects.create(**nota)


def populate_database():
    create_user()
    populate_database_clientes()
    pupulate_database_notas()


populate_database()
