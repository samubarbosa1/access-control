import re
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
import uuid
import os
from PIL import Image

def upload_to(instance, filename):
    # Salva o arquivo em MEDIA_ROOT/photos/pessoa_<id>/<filename>
    return os.path.join('photos', f'pessoa_{instance.id}', filename)


def validate_image(file):
    valid_mime_types = ['image/jpeg', 'image/png', 'image/gif']
    valid_extensions = ['jpg', 'jpeg', 'png', 'gif']

    # Verifica a extensão do arquivo
    extension = os.path.splitext(file.name)[1][1:].lower()
    if extension not in valid_extensions:
        raise ValidationError('Tipo de arquivo não suportado. As extensões permitidas são: jpg, jpeg, png, gif.')

    # Verifica o tipo MIME
    if hasattr(file, 'content_type'):
        mime_type = file.content_type
        if mime_type not in valid_mime_types:
            raise ValidationError('Tipo de arquivo não suportado. Os tipos permitidos são: image/jpeg, image/png, image/gif.')

    # Verifica se é realmente uma imagem
    try:
        # Tenta abrir o arquivo como uma imagem
        image = Image.open(file)
        image.verify()  # Verifica se é uma imagem válida
    except Exception:
        raise ValidationError('O arquivo não é uma imagem válida.')
    

"""model para representar uma ação que será monitorada"""
class Pessoa(models.Model):
    cpf = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=255)
    qr_code = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    foto = models.ImageField(
        upload_to=upload_to, 
        blank=True, 
        null=True,
        validators=[validate_image],  # Adiciona a validação personalizada
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Gera um QR Code único se não for fornecido
        if not self.qr_code:
            self.qr_code = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def verify_cpf(self):
        pass
    
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
    motorista = models.ForeignKey(
        Militar, on_delete=models.SET_NULL, null=True, blank=True, related_name="registros_como_motorista"
    )
    chefe_viatura = models.ForeignKey(
        Militar, on_delete=models.SET_NULL, null=True, blank=True, related_name="registros_como_chefe"
    )
    odometro = models.PositiveIntegerField(null=True, blank=True)  # Apenas para viaturas
    militar = models.ForeignKey(
        Militar, on_delete=models.SET_NULL, null=True, blank=True, related_name="registros_acesso_militar"
    )
    visitante = models.ForeignKey(
        Visitante, on_delete=models.SET_NULL, null=True, blank=True, related_name="registros_acesso_visitante"
    )
    viatura_administrativa = models.ForeignKey(
        ViaturaAdministrativa, on_delete=models.SET_NULL, null=True, blank=True, related_name='registros_viatura_adm'
    )
    viatura_operacional = models.ForeignKey(
        ViaturaOperacional, on_delete=models.SET_NULL, null=True, blank=True, related_name='registros_viatura_op'
    )
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo_acesso} - {self.qr_code} - Entrada: {self.data_hora_entrada}"



@receiver(pre_save, sender=Militar)
def delete_old_file_militar(sender, instance, **kwargs):
    if not instance.pk:
        return False  # Objeto novo, sem foto antiga

    try:
        old_file = Militar.objects.get(pk=instance.pk).foto
    except Militar.DoesNotExist:
        return False

    # Compara a foto antiga com a nova
    file = instance.foto
    if not old_file == file:
        if old_file:
            if old_file.storage.exists(old_file.name):
                old_file.delete(save=False)


@receiver(pre_save, sender=Visitante)
def delete_old_file_visitante(sender, instance, **kwargs):
    if not instance.pk:
        return False  # Objeto novo, sem foto antiga

    try:
        old_file = Visitante.objects.get(pk=instance.pk).foto
    except Visitante.DoesNotExist:
        return False

    # Compara a foto antiga com a nova
    file = instance.foto
    if not old_file == file:
        if old_file:
            if old_file.storage.exists(old_file.name):
                old_file.delete(save=False)

@receiver(post_delete, sender=Militar)
def delete_file_on_delete_militar(sender, instance, **kwargs):
    if instance.foto:
        if instance.foto.storage.exists(instance.foto.name):
            instance.foto.delete(save=False)

@receiver(post_delete, sender=Visitante)
def delete_file_on_delete_visitante(sender, instance, **kwargs):
    if instance.foto:
        if instance.foto.storage.exists(instance.foto.name):
            instance.foto.delete(save=False)
