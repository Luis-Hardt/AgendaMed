from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib import messages
from datetime import timedelta

from .models import Exame, ExameFinalizado
from .forms import ExameForm


salas = 3

def home(request):
    return render(request, 'exames/index.html')

def finalizar_exame(exame, status='A'):
    ExameFinalizado.objects.create(
        codigo=exame.pk,
        nome=exame.nome,
        data_cadastro=exame.data_cadastro,
        inicio_atendimento=exame.inicio_atendimento,
        status=status
    )
    exame.delete()


def cancelar_exames_antigos():
    limite_tempo = timezone.now() - timedelta(minutes=15)

    exames_expirados = Exame.objects.filter(
        sala_atendimento__isnull=False,
        inicio_atendimento__lt=limite_tempo
    )

    for exame in exames_expirados:
        finalizar_exame(exame, status='C')


def fila_exames(request):
    cancelar_exames_antigos()

    exames_em_sala = Exame.objects.filter(sala_atendimento__isnull=False).order_by('sala_atendimento')
    salas_ocupadas = set(exames_em_sala.values_list('sala_atendimento', flat=True))
    salas_disponiveis = [i for i in range(1, salas + 1) if i not in salas_ocupadas]

    exames_na_fila = Exame.objects.filter(sala_atendimento__isnull=True).order_by('data_cadastro')

    for sala_num in salas_disponiveis:
        if exames_na_fila:
            exame = exames_na_fila[0]
            exame.sala_atendimento = sala_num
            exame.inicio_atendimento = timezone.now()
            exame.save()
            exames_na_fila = exames_na_fila[1:]

    em_atendimento = []
    for i in range(1, salas + 1):
        exame = Exame.objects.filter(sala_atendimento=i).first()
        em_atendimento.append((i, exame))

    aguardando = Exame.objects.filter(sala_atendimento__isnull=True).order_by('data_cadastro')

    return render(request, 'exames/admin_fila_exames.html', {
        'em_atendimento': em_atendimento,
        'aguardando': aguardando,
        'salas': salas,
    })


def criar_exame(request):
    if request.method == 'POST':
        form = ExameForm(request.POST)
        if form.is_valid():
            exame = form.save()
            return redirect('exame_sucesso', pk=exame.pk)
    else:
        form = ExameForm()
    
    return render(request, 'exames/exame_form.html', {
        'form': form,
        'titulo': 'Criar Exame',
        'botao': 'Salvar'
    })


def exame_sucesso(request, pk):
    exame = get_object_or_404(Exame, pk=pk)
    return render(request, 'exames/exame_sucesso.html', {'exame': exame})


def editar_exame(request, pk):
    exame = get_object_or_404(Exame, pk=pk)
    if request.method == 'POST':
        form = ExameForm(request.POST, instance=exame)
        if form.is_valid():
            form.save()
            return redirect('admin_fila_exames')
    else:
        form = ExameForm(instance=exame)
    return render(request, 'exames/exame_form.html', {
        'form': form,
        'titulo': f'Editar Exame #{exame.pk:04d}',
        'exame': exame,
        'botao': 'Salvar Alterações'
    })


def excluir_exame(request, pk):
    exame = get_object_or_404(Exame, pk=pk)
    if request.method == 'POST':
        exame.delete()
        return redirect('admin_fila_exames')
    return render(request, 'exames/exame_excluir.html', {'exame': exame})


def detalhe_exame(request, pk):
    exame = get_object_or_404(Exame, pk=pk)
    return render(request, 'exames/exame_detalhes.html', {'exame': exame})


@require_POST
def concluir_exame(request, pk):
    exame = get_object_or_404(Exame, pk=pk)
    messages.success(request, "Exame concluído com sucesso!")
    finalizar_exame(exame, status='A')
    return redirect('admin_fila_exames')


def exames_concluidos(request):
    exames = ExameFinalizado.objects.all().order_by('-data_cadastro')[:10]
    return render(request, 'exames/exames_concluidos.html', {'exames': exames})


def fila_publica(request):
    em_atendimento = []

    for sala_num in range(1, salas + 1):
        exame = Exame.objects.filter(sala_atendimento=sala_num).order_by('-inicio_atendimento').first()
        em_atendimento.append((sala_num, exame))

    aguardando = Exame.objects.filter(sala_atendimento__isnull=True).order_by('data_cadastro')

    return render(request, 'exames/public_fila_exames.html', {
        'em_atendimento': em_atendimento,
        'aguardando': aguardando,
        'salas': salas,
    })
