from django.db import models
from clientes.models import Clientes


# Create your models here.
class Nota(models.Model):
    """
    Modelo de Nota

    Campos
    - cliente: ForeignKey - Cliente relacionado à nota
    - title: CharField - Título da nota
    - description: TextField - Descrição da nota
    - created_at: DateTimeField - Data de criação da nota
    - updated_at: DateTimeField - Data de atualização da nota

    Campos de criação
    - created_at: DateTimeField - Data de criação da nota
    - updated_at: DateTimeField - Data de atualização da nota
    """

    cliente = models.ForeignKey(
        Clientes, on_delete=models.CASCADE, null=False, blank=False
    )
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.title} - {self.description}"
