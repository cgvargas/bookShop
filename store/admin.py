from django.contrib import admin
from .models import Produto, Cliente, ClienteSenha
from django.urls import path, include


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email')
    search_fields = ('nome', 'email')


admin.site.register(Produto)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(ClienteSenha)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.url')),  # Inclua suas URLs aqui
]

