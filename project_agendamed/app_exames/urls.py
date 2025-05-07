from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('exames/', ExameListView.as_view(), name='exame-list'),
    path('exames/novo/', ExameCreateView.as_view(), name='exame-create'),
    path('exames/<int:pk>/', ExameDetailView.as_view(), name='exame-detail'),
    path('exames/<int:pk>/atualizar/', ExameUpdateView.as_view(), name='exame-update'),
    path('exames/<int:pk>/deletar/', ExameDeleteView.as_view(), name='exame-delete'),
]