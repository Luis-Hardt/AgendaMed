from django import forms
from .models import Exame

class ExameForm(forms.ModelForm):
    class Meta:
        model = Exame
        fields = [
            'nome',
            'data_nascimento',
            'genero',
            'cpf',
        ]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'})
        }