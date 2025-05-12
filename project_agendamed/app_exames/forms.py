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
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
            }),
            'genero': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
        }