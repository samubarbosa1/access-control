from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MilitarViewSet,
    VisitanteViewSet,
    ViaturaAdministrativaViewSet,
    ViaturaOperacionalViewSet,
    RegistroAcessoViewSet,
)

router = DefaultRouter()
router.register('militares', MilitarViewSet)
router.register('visitantes', VisitanteViewSet)
router.register('viaturas-administrativas', ViaturaAdministrativaViewSet)
router.register('viaturas-operacionais', ViaturaOperacionalViewSet)
router.register('registros-acesso', RegistroAcessoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
