from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('fila/admin/', views.fila_exames, name='admin_fila_exames'),
    path('fila/cadastrar/', views.criar_exame, name='exame_criar'),
    path('fila/info=<int:pk>/', views.detalhe_exame, name='exame_detalhes'),
    path('fila/sucesso=<int:pk>/', views.exame_sucesso, name='exame_sucesso'),
    path('fila/editar=<int:pk>/', views.editar_exame, name='exame_editar'),
    path('fila/excluir=<int:pk>/', views.excluir_exame, name='exame_excluir'),
    path('fila/concluir=<int:pk>/', views.concluir_exame, name='exame_concluir'),

    path('fila/', views.fila_publica, name='public_fila_exames'),
    path('concluidos/', views.exames_concluidos, name='public_exames_concluidos'),
]
