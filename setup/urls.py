from django.contrib import admin
from django.urls import path, include
from clientes.urls import cliente_router
from auth_user.views import CustomAuthToken
from nota.urls import router as nota_router
from rest_framework import routers

routers = routers.DefaultRouter()
routers.registry.extend(cliente_router.registry)
routers.registry.extend(nota_router.registry)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(routers.urls)),
    path("api-auth/login/", CustomAuthToken.as_view()),
]
