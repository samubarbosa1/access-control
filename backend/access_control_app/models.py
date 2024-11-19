import re
from django.db import models
from django.core.exceptions import ValidationError
import uuid

"""model para representar uma ação que será monitorada"""
class Pessoa(models.Model):
    cpf = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=255)
    qr_code = models.CharField(max_length=255, unique=True, default=uuid.uuid4)

    def verify_cpf(self):
        pass

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.nome_completo


class Militar(Pessoa):
    patente = models.CharField(max_length=50)
    id_mil = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.patente} {self.nome_completo}"


class Visitante(Pessoa):
    destino = models.CharField(max_length=200)
    observacoes = models.TextField(blank=True, null=True)

    def verify_cpf(self):
        pass

    def __str__(self):
        return f"{self.nome_completo} (Visitante)"


# Classe base para Viaturas
class Viatura(models.Model):
    modelo = models.CharField(max_length=50)
    tipo = models.CharField(max_length=20)  # Administrativa ou Operacional

    class Meta:
        abstract = True  # Define como modelo abstrato, não cria tabela no banco


# Viatura Administrativa
class ViaturaAdministrativa(Viatura):
    placa = models.CharField(max_length=7, unique=True)

    def __str__(self):
        return f"Administrativa - {self.numero_eb} ({self.placa})"


# Viatura Operacional
class ViaturaOperacional(Viatura):
    eb_placa = models.CharField(max_length=10, unique=True)

    def clean(self):
        # Validação de EB-placa padrão: 1123412341
        if not re.match(r'^\d{10}$', self.eb_placa):
            raise ValidationError("EB-Placa inválida. Deve conter exatamente 10 dígitos.")

    def __str__(self):
        return f"Operacional - {self.numero_eb} ({self.eb_placa})"


class RegistroAcesso(models.Model):
    TIPOS_ACESSO = [
        ('MILITAR', 'Militar'),
        ('VTR_ADM', 'Viatura Administrativa'),
        ('VTR_OP', 'Viatura Operacional'),
        ('VISITANTE', 'Visitante'),
    ]
    tipo_acesso = models.CharField(max_length=10, choices=TIPOS_ACESSO)
    data_hora_entrada = models.DateTimeField(auto_now_add=True)
    data_hora_saida = models.DateTimeField(blank=True, null=True)
    qr_code = models.CharField(max_length=255)  # QR Code lido
    motorista = models.ForeignKey(
        Militar, on_delete=models.SET_NULL, null=True, blank=True, related_name="registros_como_motorista"
    )
    chefe_viatura = models.ForeignKey(
        Militar, on_delete=models.SET_NULL, null=True, blank=True, related_name="registros_como_chefe"
    )
    odometro = models.PositiveIntegerField(null=True, blank=True)  # Apenas para viaturas
    observacoes = models.TextField(blank=True, null=True)
    viatura_administrativa = models.ForeignKey(
        ViaturaAdministrativa, on_delete=models.SET_NULL, null=True, blank=True
    )
    viatura_operacional = models.ForeignKey(
        ViaturaOperacional, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.tipo_acesso} - {self.qr_code} - Entrada: {self.data_hora_entrada}"

