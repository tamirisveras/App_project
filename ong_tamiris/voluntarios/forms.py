from django import forms
from .models import UserVoluntario
from django.contrib.auth.models import User

class EditUserVoluntarioForm(forms.ModelForm):
        
    first_name = forms.CharField(label='Nome', max_length=100, required=False)
    last_name = forms.CharField(label='Sobrenome', max_length=100, required=False)
    foto = forms.ImageField(label='Foto', required=False)
    sexo = forms.ChoiceField(required=False, choices=UserVoluntario.SEXO_CHOICES)
    nascimento = forms.DateField(label='Data de Nascimento', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].choices = self.get_active_user()
    
    @staticmethod
    def get_active_user():
        return [(users.id, users.username) for users in User.objects.filter(is_superuser=False).all()]

    class Meta:
        model = UserVoluntario
        fields = ['foto', 'sexo', 'nascimento','user']

    def clean_foto(self):
        foto = self.cleaned_data.get('foto', None)
        if foto:
            if not foto.content_type or 'image' not in foto.content_type:
                raise forms.ValidationError('O arquivo enviado não é uma imagem.')
        return foto

    def save(self, commit=True):
        user_id = self.cleaned_data['user'].id
        user = User.objects.get(pk=user_id)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return super().save(commit=commit)


class UserVoluntarioForm(forms.ModelForm):
    
    first_name = forms.CharField(label='Nome', max_length=100)
    last_name = forms.CharField(label='Sobrenome', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Senha', max_length=100, widget=forms.PasswordInput)


    class Meta:
        model = UserVoluntario
        fields = ['foto', 'sexo', 'nascimento']


    def save(self, commit=True):
        user  = User.objects.create_user(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        voluntario = super().save(commit=False)
        voluntario.user = user
        if commit:
            voluntario.save()
        return voluntario
