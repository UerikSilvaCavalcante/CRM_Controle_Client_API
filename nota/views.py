from rest_framework import viewsets, filters
from nota.models import Nota
from clientes.models import Clientes
from nota.serializers import NotaSerializer
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.
class NotaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para o modelo Nota

    Campos de pesquisa:
    - cliente__id:int - ID do cliente
    - cliente__name:str - Nome do cliente

    Serializer: NotaSerializer

    """

    serializer_class = NotaSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    search_fields = ["cliente__id", "cliente__name"]

    def get_queryset(self):  # type: ignore
        if self.request.user.is_superuser:
            queryset = Nota.objects.all()
        else:
            queryset = (
                Nota.objects.filter(cliente__responsavel=self.request.user)
                .order_by("created_at")
                .all()
            )
        return queryset
