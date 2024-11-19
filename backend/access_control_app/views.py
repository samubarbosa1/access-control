from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Militar, Visitante, ViaturaAdministrativa, ViaturaOperacional, RegistroAcesso
from .serializers import (
    MilitarSerializer, 
    VisitanteSerializer, 
    ViaturaAdministrativaSerializer, 
    ViaturaOperacionalSerializer, 
    RegistroAcessoSerializer
)
import uuid

# ViewSet para Militar
class MilitarViewSet(viewsets.ModelViewSet):
    queryset = Militar.objects.all()
    serializer_class = MilitarSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        if 'qr_code' not in data or not data['qr_code']:
            data['qr_code'] = str(uuid.uuid4())  # Generate a unique QR code
        return super().create(request, *args, **kwargs)

# ViewSet para Visitante
class VisitanteViewSet(viewsets.ModelViewSet):
    queryset = Visitante.objects.all()
    serializer_class = VisitanteSerializer

# ViewSet para Viatura Administrativa
class ViaturaAdministrativaViewSet(viewsets.ModelViewSet):
    queryset = ViaturaAdministrativa.objects.all()
    serializer_class = ViaturaAdministrativaSerializer

# ViewSet para Viatura Operacional
class ViaturaOperacionalViewSet(viewsets.ModelViewSet):
    queryset = ViaturaOperacional.objects.all()
    serializer_class = ViaturaOperacionalSerializer

# ViewSet para Registro de Acesso
class RegistroAcessoViewSet(viewsets.ModelViewSet):
    queryset = RegistroAcesso.objects.all()
    serializer_class = RegistroAcessoSerializer

    # Sobrescrevendo create para lógica personalizada
    def create(self, request, *args, **kwargs):
        data = request.data
        tipo_acesso = data.get('tipo_acesso')

        # Validações adicionais para Viatura
        if tipo_acesso in ['VTR_ADM', 'VTR_OP']:
            if 'odometro' not in data or not data['odometro']:
                return Response(
                    {"error": "O campo 'odometro' é obrigatório para viaturas."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if 'motorista' not in data or not data['motorista']:
                return Response(
                    {"error": "O campo 'motorista' é obrigatório para viaturas."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validações para chefe de viatura em viaturas não administrativas
            if tipo_acesso == 'VTR_OP' and ('chefe_viatura' not in data or not data['chefe_viatura']):
                return Response(
                    {"error": "O campo 'chefe_viatura' é obrigatório para viaturas operacionais."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return super().create(request, *args, **kwargs)
