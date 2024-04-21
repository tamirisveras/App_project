from django.urls import path
from .views import (
    VoluntarioDetailView, VoluntarioCreateView, VoluntarioUpdateView
    ,VoluntarioDeleteView, Login, Logout, ListProjetosView, IncricaoProjeto)
from django.views.generic import TemplateView

urlpatterns = [
    path('voluntary/project/<int:pk>', IncricaoProjeto.as_view(), name='subscribe'),
    path('voluntary/project/', ListProjetosView.as_view(), name='project'),
    path('voluntary/', TemplateView.as_view(template_name = 'voluntary/home_voluntary.html'), name='voluntary'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('voluntary/<int:pk>/', VoluntarioDetailView.as_view(), name='voluntary_detail'),
    path('voluntary/new/', VoluntarioCreateView.as_view(), name='voluntary_new'),
    path('voluntary/<int:pk>/edit/', VoluntarioUpdateView.as_view(), name='voluntary_edit'),
    path('voluntary/<int:pk>/delete/', VoluntarioDeleteView.as_view(), name='voluntary_delete'),
]
