from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import ContatoForms, ClienteForm, SenhaForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required

from .models import Produto, CartItem, Cliente, Estado


def home(request):
    products = Produto.objects.all()  # Renomeado para evitar confusão
    return render(request, 'home.html', {'products': products})


def contato(request):
    form = ContatoForms(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            nome = form.cleaned_data['nome']
            email = form.cleaned_data['email']
            assunto = form.cleaned_data['assunto']
            mensagem = form.cleaned_data['mensagem']

            messages.success(request, 'E-mail enviado com sucesso!')
            form = ContatoForms()
        else:
            messages.error(request, 'Erro ao enviar e-mail')

    context = {'form': form}
    return render(request, 'contact.html', context)


def sobre(request):
    return render(request, 'about.html')


def product_detail(request, product_id):
    product = get_object_or_404(Produto, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})


@login_required
def carrinho(request):
    cart_items = CartItem.objects.filter(usuario=request.user)
    total_cost = sum(item.produto.preco * item.quantidade_no_carrinho for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
    }

    return render(request, 'cart.html', context)


def adicionar_ao_carrinho(request, product_id):
    product = get_object_or_404(Produto, pk=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        produto=product,
        usuario=request.user,
        defaults={'quantidade_no_carrinho': 0}
    )
    cart_item.quantidade_no_carrinho += 1
    cart_item.save()

    return redirect('carrinho')


def remover_carrinho(request, product_id):
    product = get_object_or_404(Produto, pk=product_id)
    cart_item = CartItem.objects.filter(produto=product, usuario=request.user).first()
    if cart_item:
        cart_item.quantidade_no_carrinho -= 1
        if cart_item.quantidade_no_carrinho == 0:
            cart_item.delete()
        else:
            cart_item.save()

    return redirect('carrinho')


@login_required
def finalizar_compra(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(usuario=request.user)
        erro = []
        produtos_comprados = []

        for item in cart_items:
            produto = item.produto
            if produto.quantidade >= item.quantidade_no_carrinho:
                produto.quantidade -= item.quantidade_no_carrinho
                produto.save()
                produtos_comprados.append(produto)
            else:
                erro.append(f"Estoque insuficiente para o produto {produto.nome}")

        cart_items.delete()

        if erro:
            return render(request, 'carrinho.html', {'erro': erro})

        return render(request, 'compra_confirmada.html', {'produtos_comprados': produtos_comprados})

    return redirect('carrinho')


def compra_confirmada(request):
    return render(request, 'compra_confirmada.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'login.html')


class CadastroClienteView(View):
    def get(self, request):
        estados = self.get_estados()  # Obter os estados
        cliente_form = ClienteForm(estados=estados)  # Formulário para o cliente
        senha_form = SenhaForm()  # Instanciando senha_form
        user_form = UserRegistrationForm()  # Instanciando user_form

        # Limpa as mensagens antigas da sessão
        storage = get_messages(request)
        for _ in storage:
            pass

        return render(request, 'cadastro.html', {
            'cliente_form': cliente_form,
            'senha_form': senha_form,
            'user_form': user_form,  # Passando a variável user_form
            'estados': estados
        })

    def post(self, request):
        estados = self.get_estados()  # Obter os estados novamente
        cliente_form = ClienteForm(request.POST, estados=estados)  # Formulário para o cliente
        senha_form = SenhaForm(request.POST)  # Instanciando senha_form com os dados POST
        user_form = UserRegistrationForm(request.POST)  # Instanciando user_form com os dados POST

        if cliente_form.is_valid() and user_form.is_valid() and senha_form.is_valid():  # Verifique os três formulários
            cliente = cliente_form.save()  # Salvar o cliente
            user = user_form.save(commit=False)  # Criar o usuário, mas não salvar ainda
            user.set_password(user_form.cleaned_data['password'])  # Define a senha de forma correta
            user.save()  # Salva o usuário no banco de dados
            messages.success(request, 'Cadastro realizado com sucesso! Agora, defina sua senha.')
            return redirect('definir_senha', cliente_id=cliente.id)

        return render(request, 'cadastro.html', {
            'cliente_form': cliente_form,
            'senha_form': senha_form,  # Passando a variável senha_form em caso de erro
            'user_form': user_form,  # Passando a variável user_form em caso de erro
            'estados': estados
        })

    def get_estados(self):
        estados = Estado.objects.all()
        return [(estado.sigla, estado.nome) for estado in estados]  # Retorna os estados


class DefinirSenhaView(View):
    def get(self, request, cliente_id):
        senha_form = SenhaForm()
        return render(request, 'definir_senha.html', {'senha_form': senha_form, 'cliente_id': cliente_id})

    def post(self, request, cliente_id):
        senha_form = SenhaForm(request.POST)
        if senha_form.is_valid():
            senha = senha_form.cleaned_data['senha']
            email = request.POST.get('email')

            usuario = User.objects.create_user(username=email, password=senha)

            cliente = Cliente.objects.get(id=cliente_id)
            cliente.usuario = usuario
            cliente.save()

            messages.success(request, 'Senha definida com sucesso! Você já pode fazer login.')
            return redirect('login')

        return render(request, 'definir_senha.html', {'senha_form': senha_form, 'cliente_id': cliente_id})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Cadastro realizado com sucesso! Agora faça login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})
