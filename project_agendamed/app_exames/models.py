from django.db import models

class Exame(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro (especifique)'),
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
    )

    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data/Hora do Cadastro',
    )

    class Meta:
        ordering = ['data_cadastro']

    def __str__(self):
        return f"EXAME {self.pk}: {self.nome}, {self.cpf} ({self.data_cadastro})"