from django.contrib import admin
from clientes.models import Clientes
# Register your models here.
@admin.register(Clientes)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    list_filter = ('created_at',)
    list_display_links = ('name', 'email',)