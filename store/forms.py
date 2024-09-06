from django import forms
from .models import Cliente
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field


class ContatoForms(forms.Form):
    nome = forms.CharField(label='Nome')
    email = forms.EmailField(label='E-mail')
    assunto = forms.CharField(label='Assunto')
    mensagem = forms.CharField(label='Mensagem', widget=forms.Textarea())


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}))

    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuário'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('username'),
            Field('password'),
            Submit('submit', 'Criar Conta', css_class='btn btn-primary'),
        )


class ClienteForm(forms.ModelForm):
    estado = forms.ChoiceField(choices=[], required=True)

    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'telefone', 'endereco', 'bairro', 'cidade', 'estado', 'cep']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome Completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estado'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP'}),
        }


class SenhaForm(forms.Form):
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}))
    confirmar_senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar Senha'}))

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        confirmar_senha = cleaned_data.get("confirmar_senha")

        if senha and confirmar_senha and senha != confirmar_senha:
            raise forms.ValidationError("As senhas não coincidem. Por favor, tente novamente.")

        return cleaned_data
