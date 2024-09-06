from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField()
    imagem = models.ImageField(upload_to='imagens/', default='imagens/default.jpg')

    def __str__(self):
        return self.nome


class CartItem(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    quantidade_no_carrinho = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.produto.nome} (x{self.quantidade_no_carrinho})"


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=14, validators=[
        RegexValidator(regex=r'^\(\d{2}\)\d{5}-\d{4}$', message='Formato do número de telefone: (00)00000-0000.')])
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=10, validators=[
        RegexValidator(regex=r'^\d{5}-?\d{3}$', message='CEP deve ser no formato 00000-000.')])
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome


# Classe que pode ser usada para criar ou atualizar a senha do cliente
class ClienteSenha(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    senha = models.CharField(max_length=128)  # Para senhas, normalmente usamos o mecanismo de hash do Django

    def __str__(self):
        return f'Senha de {self.cliente.nome}'


"""
Descrição das Classes:

Cadastro:

- nome: Armazena o nome completo do cliente.
- email: E-mail único para cada cliente (impede duplicidade).
- telefone: Armazena o telefone do cliente, com validação de formato.
- endereco: Campo para o endereço do cliente.
- cidade: Campo para a cidade.
- estado: Abreviação do estado.
- cep: Campo para o código postal com validação.
- usuario: Um campo para conectar ao modelo de Usuário do Django, caso você use autenticação.

ClienteSenha:

- Um modelo opcional para armazenar a senha do cliente separadamente, permitindo que você possa definir 
  a senha após o preenchimento do formulário.
  
"Observações":
- Ao cadastrar e armazenar senhas, você deve usar sempre hashing! O Django oferece métodos nativos para isso 
  (como make_password e check_password).
- Em uma aplicação real, você provavelmente irá querer criar um processo para enviar uma confirmação de senha 
  após o cadastro.
"""