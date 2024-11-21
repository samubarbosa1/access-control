from rest_framework import serializers
from .models import Militar, Visitante, ViaturaAdministrativa, ViaturaOperacional, RegistroAcesso
from PIL import Image

class MilitarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Militar
        fields = '__all__'
        read_only_fields = ['qr_code']

    def validate_foto(self, value):
        try:
            image = Image.open(value)
            image.verify()
        except Exception:
            raise serializers.ValidationError('O arquivo não é uma imagem válida.')
        return value

class VisitanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitante
        fields = '__all__'
        read_only_fields = ['qr_code']
    
    def validate_foto(self, value):
        from PIL import Image
        try:
            image = Image.open(value)
            image.verify()
        except Exception:
            raise serializers.ValidationError('O arquivo não é uma imagem válida.')
        return value

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
