from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='E-mail',
        error_messages={'unique': 'Um usuário com este e-mail já existe.'}
    )
    first_name = forms.CharField(
        required=True,
        label='Nome',
        max_length=30
    )
    last_name = forms.CharField(
        required=True,
        label='Sobrenome',
        max_length=30
    )

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")
        labels = {
            'username': _('Nome de usuário'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].label = 'Confirme a senha'
        self.fields['username'].help_text = 'Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.'
        self.fields['password1'].help_text = 'Sua senha deve conter pelo menos 8 caracteres e não pode ser inteiramente numérica.'
        self.fields['password2'].help_text = 'Digite a mesma senha novamente, para verificação.'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este e-mail já está em uso.")
        return email
