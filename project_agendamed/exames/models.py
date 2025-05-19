from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

class Exame(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
        ('N', 'Prefiro não dizer'),
    ]

    nome = models.CharField(
        max_length=100,
        verbose_name='Nome Completo',
    )
    data_nascimento = models.DateField(
        verbose_name='Data de Nascimento',
    )
    genero = models.CharField(
        max_length=1,
        choices=GENERO_CHOICES,
        verbose_name='Gênero',
    )
    cpf = models.CharField(
        max_length=11,
        verbose_name='CPF',
        unique=True,
        validators=[RegexValidator(r'^\d{11}$', 'CPF deve conter exatamente 11 dígitos numéricos')],
    )

    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data/Hora do Cadastro',
    )
    inicio_atendimento = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data/Hora do Início de Atendimento',
    )
    sala_atendimento = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['-data_cadastro']

    def __str__(self):
        return f"EXAME {self.pk}: {self.nome}, {self.cpf} ({self.data_cadastro})"

    def clean(self):
        if self.data_nascimento and self.data_nascimento > timezone.now().date():
            raise ValidationError({'data_nascimento': 'Data de nascimento inválida.'})


class ExameFinalizado(models.Model):
    STATUS_CHOICES = [
        ('A', 'Atendido'),
        ('C', 'Cancelado'),
    ]

    codigo = models.IntegerField()
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome Completo',
        default="",
    )
    data_cadastro = models.DateTimeField()
    inicio_atendimento = models.DateTimeField(null=True, blank=True)
    data_finalizacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')

    class Meta:
        verbose_name = 'Exame Concluído'
        verbose_name_plural = 'Exames Concluídos'
        ordering = ['-data_finalizacao']

    def __str__(self):
        return f"EXAME {self.codigo}: {self.nome}, {self.cpf} ({self.data_cadastro}) - {self.get_status_display()}"