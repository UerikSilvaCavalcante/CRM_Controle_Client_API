import os
import sys
import django

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
django.setup()


from clientes.models import Clientes
from django.contrib.auth.models import User
from nota.models import Nota


def populate_database_clientes():
    clientes = (
        {
            "name": "João",
            "email": "jE0k4@example.com",
            "phone": "1234567890",
            "responsavel_id": 1,
        },
        {
            "name": "Pedro",
            "email": "pE3k4@example.com",
            "phone": "9876543210",
            "responsavel_id": 1,
        },
        {
            "name": "Ana",
            "email": "aE2k4@example.com",
            "phone": "5555555555",
            "responsavel_id": 1,
        },
        {
            "name": "Maria",
            "email": "1e2dI@example.com",
            "phone": "1234567890",
            "responsavel_id": 1,
        },
    )
    for cliente in clientes:
        Clientes.objects.create(**cliente)


def pupulate_database_notas():
    notas = (
        {"title": "Nota 1", "description": "Descrição da nota 1", "cliente_id": 1},
        {"title": "Nota 2", "description": "Descrição da nota 2", "cliente_id": 1},
        {"title": "Nota 3", "description": "Descrição da nota 3", "cliente_id": 2},
        {"title": "Nota 4", "description": "Descrição da nota 4", "cliente_id": 2},
    )
    for nota in notas:
        Nota.objects.create(**nota)


def populate_database():
    
    populate_database_clientes()
    pupulate_database_notas()


populate_database()
