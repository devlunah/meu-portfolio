# app/admin.py
from django.contrib import admin
from .models import Pessoa

@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ("nome", "cpf", "email", "telefone", "cidade", "uf", "ativo", "criado_em")
    list_filter = ("ativo", "uf", "sexo")
    search_fields = ("nome", "cpf", "email", "telefone", "cidade", "bairro")
