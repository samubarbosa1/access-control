from rest_framework import viewsets, status
from rest_framework.decorators import api_view
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
from django.utils import timezone
from rest_framework.parsers import MultiPartParser, FormParser

# ViewSet para Militar
class MilitarViewSet(viewsets.ModelViewSet):
    queryset = Militar.objects.all()
    serializer_class = MilitarSerializer
    parser_classes = (MultiPartParser, FormParser) 

# ViewSet para Visitante
class VisitanteViewSet(viewsets.ModelViewSet):
    queryset = Visitante.objects.all()
    serializer_class = VisitanteSerializer
    parser_classes = (MultiPartParser, FormParser) 

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


@api_view(['POST'])
def registrar_acesso_qr_code(request):
    qr_code = request.data.get('qr_code')

    if not qr_code:
        return Response({'error': 'QR Code é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

    tipo_acesso, codigo = qr_code.split(':')

    if(tipo_acesso == "MILITAR"):
        militar = Militar.objects.get(qr_code=codigo)
        if not militar:
            Response({'error': 'Código não reconhecido'}, status=status.HTTP_400_BAD_REQUEST)

        open_record = RegistroAcesso.objects.filter(
            militar=militar,
            data_hora_saida__isnull=True
        ).last()
    
    elif(tipo_acesso == "VISITANTE"):
        visitante = Visitante.objects.get(qr_code=codigo)
        if not visitante:
            Response({'error': 'Código não reconhecido'}, status=status.HTTP_400_BAD_REQUEST)
        open_record = RegistroAcesso.objects.filter(
            visitante=visitante,
            data_hora_saida__isnull=True
        ).last()

    if open_record:
        open_record.data_hora_saida = timezone.now()
        open_record.save()
        return Response({'message': 'Saída registrada com sucesso.'}, status=status.HTTP_200_OK)
    
    registro = RegistroAcesso(
        tipo_acesso=tipo_acesso,
        data_hora_entrada=timezone.now(),
    )
    if tipo_acesso == 'MILITAR':
        registro.militar = militar
    elif tipo_acesso == 'VISITANTE':
        registro.visitante = visitante
    registro.save()
    return Response({'message': 'Entrada registrada com sucesso.'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def registrar_acesso_viatura(request):
    
    data = request.data
    tipo_acesso = data['tipo_acesso']
    viatura_adm = data['viatura_administrativa']
    viatura_op = data['viatura_operacional']
    motorista = data['motorista']
    chefe_viatura = data['chefe_viatura']
    observacoes = data['observacoes']
    entrada_saida = data['entrada_saida']
    odometro = data['odometro']

    motorista = Militar.objects.get(id=motorista)
    chefe_viatura = Militar.objects.get(id= chefe_viatura)

    if(not motorista or not chefe_viatura):
        return Response({'error': 'Motorista ou chefe de viatura não encontrados.'}, status=status.HTTP_400_BAD_REQUEST)

    registro = RegistroAcesso(
        tipo_acesso = tipo_acesso,
        motorista = motorista,
        chefe_viatura = chefe_viatura,
        )
    
    if(entrada_saida == "ENTRADA"):
        registro.data_hora_entrada = timezone.now()
    elif(entrada_saida == "SAIDA"):
        registro.data_hora_saida = timezone.now()
    else:
        return Response({'error': 'Entrada ou saída devem ser especificadas.'}, status=status.HTTP_400_BAD_REQUEST)
    if viatura_adm:
        viatura_adm = ViaturaAdministrativa.objects.get(id = viatura_adm)
        registro.viatura_administrativa = viatura_adm
    else: 
        viatura_op = ViaturaOperacional.objects.get(id = viatura_op)
        registro.viatura_operacional = viatura_op
    registro.observacoes = observacoes
    registro.odometro = odometro
    registro.save()
    
    return Response({'message': f'{entrada_saida.lower()} registrada com sucesso.'}, status=status.HTTP_201_CREATED)


