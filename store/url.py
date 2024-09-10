# store/url.py
from django.urls import path
from .views import home, contato, sobre, product_detail, carrinho, user_login, register, finalizar_compra, \
    adicionar_ao_carrinho, remover_carrinho, compra_confirmada, CadastroClienteView, DefinirSenhaView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('contato/', contato, name='contato'),
    path('sobre/', sobre, name='sobre'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('adicionar_ao_carrinho/<int:product_id>/', adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('remover_carrinho/<int:product_id>/', remover_carrinho, name='remover_carrinho'),
    path('carrinho/', carrinho, name='carrinho'),
    path('finalizar_compra/', finalizar_compra, name='finalizar_compra'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    # Logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('compra_confirmada/', compra_confirmada, name='compra_confirmada'),
    path('cadastro/', CadastroClienteView.as_view(), name='cadastro'),
    path('definir_senha/<int:cliente_id>/', DefinirSenhaView.as_view(), name='definir_senha'),

]
