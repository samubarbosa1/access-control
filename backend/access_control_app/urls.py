from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MilitarViewSet,
    VisitanteViewSet,
    ViaturaAdministrativaViewSet,
    ViaturaOperacionalViewSet,
    RegistroAcessoViewSet,
    registrar_acesso_qr_code,
    registrar_acesso_viatura
)   

router = DefaultRouter()
router.register('militares', MilitarViewSet)
router.register('visitantes', VisitanteViewSet)
router.register('viaturas-administrativas', ViaturaAdministrativaViewSet)
router.register('viaturas-operacionais', ViaturaOperacionalViewSet)
router.register('registros-acesso', RegistroAcessoViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('registrar-acesso-qr-code/', registrar_acesso_qr_code, name='registrar_acesso_qr_code'),
    path('registrar-acesso-viatura/', registrar_acesso_viatura, name='registrar_acesso_viatura'),
]
