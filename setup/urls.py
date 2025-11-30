from django.contrib import admin
from django.urls import path, include
from clientes.urls import cliente_router
from nota.urls import router as nota_router
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Documentação API",
        default_version="v1",
        description="Documentação da API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="yV4yH@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    authentication_classes=[],
)


routers = routers.DefaultRouter()
routers.registry.extend(cliente_router.registry)
routers.registry.extend(nota_router.registry)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(routers.urls)),
    path("api-auth/", include("auth_user.urls")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
