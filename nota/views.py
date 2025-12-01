from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from nota.models import Nota
from nota.serializers import NotaSerializer
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from nota.permissions import IsAdminOrVendedorOwner
from auth_user.authenticate_cliente import ClienteAuthentication
from rest_framework.exceptions import PermissionDenied


# Create your views here.
class NotaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para o modelo Nota

    Campos de pesquisa:
    - cliente__id:int - ID do cliente
    - cliente__name:str - Nome do cliente

    Serializer: NotaSerializer

    """

    authentication_classes = [
        TokenAuthentication,
        BasicAuthentication,
        ClienteAuthentication,
    ]
    permission_classes = [IsAdminOrVendedorOwner]

    serializer_class = NotaSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    search_fields = ["cliente__id", "cliente__name"]

    def get_object(self):  # type: ignore
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):  # type: ignore
        if not isinstance(self.request.user, str):
            if self.request.user.is_superuser:
                queryset = Nota.objects.all()
            elif self.request.user.groups.filter(name="Vendedor").exists():
                queryset = (
                    Nota.objects.filter(cliente__responsavel=self.request.user)
                    .order_by("created_at")
                    .all()
                )
            else:
                raise PermissionDenied
        else:
            queryset = (
                Nota.objects.filter(cliente__email=self.request.user)  # type: ignore
                .order_by("created_at")
                .all()
            )
        return queryset
