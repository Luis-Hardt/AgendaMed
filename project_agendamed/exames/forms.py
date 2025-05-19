from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Exame

class ExameForm(forms.ModelForm):
    class Meta:
        model = Exame
        fields = ['nome', 'data_nascimento', 'genero', 'cpf']
        widgets = {
            'data_nascimento': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'
            ),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-select'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.fields['data_nascimento'].input_formats = ['%Y-%m-%d']

    def clean_data_nascimento(self):
        data = self.cleaned_data.get('data_nascimento')
        if data and data > timezone.now().date():
            raise ValidationError('Data de nascimento inválida.')
        return data

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf and (not cpf.isdigit() or len(cpf) != 11):
            raise ValidationError('CPF deve conter exatamente 11 dígitos numéricos.')
        return cpf
