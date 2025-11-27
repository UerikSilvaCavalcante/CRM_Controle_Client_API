from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Clientes(models.Model):
    """
    Modelo de Clientes

    Campos
    - name: str - Nome do cliente
    - email: str - Email do cliente
    - phone: str - Telefone do cliente

    Campos de criação
    - created_at: datetime - Data de criação do cliente
    """

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    responsavel = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self) -> str:
        return f"{self.name} - {self.email}"
