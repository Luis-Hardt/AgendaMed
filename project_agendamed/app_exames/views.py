from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import Exame
from .forms import ExameForm

class HomeView(TemplateView):
    template_name = 'app_exames/home.html'

class ExameListView(ListView):
    model = Exame
    template_name = 'app_exames/exame_list.html'
    context_object_name = 'exames'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['first_form'] = Exame.objects.first()
        return context

class ExameDetailView(DetailView):
    model = Exame
    template_name = 'app_exames/exame_detail.html'
    context_object_name = 'exame'

class ExameCreateView(CreateView):
    model = Exame
    form_class = ExameForm
    template_name = 'app_exames/exame_form.html'
    success_url = reverse_lazy('exame-list')

class ExameUpdateView(UpdateView):
    model = Exame
    form_class = ExameForm
    template_name = 'app_exames/exame_form.html'
    context_object_name = 'exame'
    def get_success_url(self):
        return reverse('exame-detail', kwargs={'pk': self.object.pk})

class ExameDeleteView(DeleteView):
    model = Exame
    template_name = 'app_exames/exame_confirm_delete.html'
    context_object_name = 'exame'
    success_url = reverse_lazy('exame-list')