from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView, View
from django.contrib.auth.views import LoginView, LogoutView
from .models import UserVoluntario, User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserVoluntarioForm, EditUserVoluntarioForm
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import ValidationError
from .models import ProjetoDoacao

class Login(LoginView):

    template_name = 'voluntary/login.html'
    success_url = reverse_lazy('voluntary')

    def get_success_url(self) -> str:
        return self.success_url
    
class Logout(LoginRequiredMixin, LogoutView):

    next_page = reverse_lazy('home')

class VoluntarioDetailView(LoginRequiredMixin, DetailView):
    
    model = User
    template_name = 'voluntary/perfil.html'
    context_object_name = 'volunt'

    def get_object(self, queryset=None):
        return get_object_or_404(UserVoluntario, user=self.request.user)

class VoluntarioCreateView(CreateView):
      
    model = UserVoluntario
    template_name = 'voluntary/voluntary_register.html'
    form_class = UserVoluntarioForm
    success_url = reverse_lazy('login')

class VoluntarioUpdateView(LoginRequiredMixin, UpdateView):
        
    model = User
    template_name = 'voluntary/voluntary_register.html'
    form_class = EditUserVoluntarioForm
    context_object_name = 'form1'

    def form_valid(self, form1):
        user = form1.save(commit=False)
        voluntario1 = UserVoluntario.objects.get(user=self.request.user)
        
        if 'foto' in form1.cleaned_data and form1.cleaned_data['foto']:
            voluntario1.foto = form1.cleaned_data['foto']
        
        voluntario1.sexo = form1.cleaned_data['sexo']
        voluntario1.nascimento = form1.cleaned_data['nascimento']
        user.first_name = form1.cleaned_data['first_name']
        user.last_name = form1.cleaned_data['last_name']
        
        try:
            user.save()
            voluntario1.save()
        except ValidationError as e:
            return self.form_invalid(form1)
        
        return super().form_valid(form1)

    
    def get_success_url(self):
        return reverse_lazy('voluntary_detail', kwargs={'pk': self.object.pk})

class VoluntarioDeleteView(LoginRequiredMixin, DeleteView):
        
    model = User
    template_name = 'voluntary/perfil.html'
    success_url = reverse_lazy('home')

    def set_valid_delete(self):
        self.request.user.delete()

    def get_object(self):
        return self.request.user
    
    def get_success_url(self) -> str:
        return self.success_url

class ListProjetosView(LoginRequiredMixin, ListView):

    model = ProjetoDoacao
    template_name = 'voluntary/project_voluntary.html'
    context_object_name = 'projetos'


class IncricaoProjeto(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        projeto = get_object_or_404(ProjetoDoacao, pk=kwargs['pk'])
        voluntario = UserVoluntario.objects.get(user=request.user)
        projeto.voluntarios.add(voluntario)
        projeto.save()
        return redirect('project')