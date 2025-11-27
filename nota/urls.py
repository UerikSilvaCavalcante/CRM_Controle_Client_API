from rest_framework import routers
from .views import NotaViewSet

router = routers.SimpleRouter()
router.register(r"notas", NotaViewSet, basename="notas")
