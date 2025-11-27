from rest_framework import routers
from clientes.views import ClientesViewSet

cliente_router = routers.SimpleRouter()

cliente_router.register(r"clientes", ClientesViewSet, basename="clientes")
