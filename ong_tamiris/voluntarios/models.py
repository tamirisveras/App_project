from django.db import models
from django.contrib.auth.models import User


class UserVoluntario(models.Model):

    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino')
    )

    foto = models.ImageField(verbose_name='Foto de Perfil', blank=True, null=True, upload_to='perfil/')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, null=False, blank=False)
    nascimento = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return self.user.email
    

class ProjetoDoacao(models.Model):

    nome = models.CharField(max_length=100, blank=False, null=False)
    descricao = models.TextField(max_length=1000, blank=False, null=False)
    data_inicio = models.DateField(blank=False, null=False, auto_now_add=True)
    data_fim = models.DateField(blank=False, null=False)
    voluntarios = models.ManyToManyField(UserVoluntario)

    def __str__(self) -> str:
        return self.nome