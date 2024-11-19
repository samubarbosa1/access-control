from rest_framework import serializers
from .models import Militar, Visitante, ViaturaAdministrativa, ViaturaOperacional, RegistroAcesso

class MilitarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Militar
        fields = '__all__'

class VisitanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitante
        fields = '__all__'

class ViaturaAdministrativaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViaturaAdministrativa
        fields = '__all__'

class ViaturaOperacionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViaturaOperacional
        fields = '__all__'

class RegistroAcessoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroAcesso
        fields = '__all__'
