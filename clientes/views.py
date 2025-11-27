from rest_framework import viewsets, filters
from clientes.models import Clientes
from clientes.serializers import ClienteSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication


# Create your views here.
class ClientesViewSet(viewsets.ModelViewSet):
    """
    ViewSet do modelo Clientes.
    Methods: GET, POST,  PUT , DELETE

    Campos de ordenação:
    - created_at:datetime - Data de criação do cliente
    - id:int - ID do cliente

    Campos de pesquisa:
    - name:str - Nome do cliente
    - email:str - Email do cliente
    - phone:str - Telefone do cliente
    - id:int - ID do cliente

    Serializer: ClienteSerializer
    """

    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    ordering_fields = ["created_at", "id"]
    search_fields = ["name", "email", "phone", "id"]
    serializer_class = ClienteSerializer

    def get_queryset(self):  # type: ignore
        queryset = (
            Clientes.objects.filter(responsavel=self.request.user)
            .order_by("created_at")
            .all()
        )
        return queryset
    