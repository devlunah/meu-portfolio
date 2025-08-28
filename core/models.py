# app/models.py
import re
from datetime import date
from django.core.validators import RegexValidator
from django.db import models

class Pessoa(models.Model):
    class Sexo(models.TextChoices):
        MASCULINO = "M", "Masculino"
        FEMININO = "F", "Feminino"
        OUTRO = "O", "Outro"
        NAO_INFORMADO = "N", "Não informado"

    nome = models.CharField("Nome completo", max_length=120)
    apelido = models.CharField("Apelido", max_length=60, blank=True)

    # CPF: armazena só dígitos (11). Unicidade garantida no banco.
    cpf = models.CharField(
        "CPF",
        max_length=11,
        unique=True,
        validators=[RegexValidator(r"^\d{11}$", "Informe 11 dígitos, somente números.")],
        help_text="Apenas números (ex.: 12345678901).",
    )

    email = models.EmailField("E-mail", unique=True, null=True, blank=True)

    # Telefone no formato internacional (E.164), ex.: +5511999999999
    telefone = models.CharField(
        "Telefone",
        max_length=17,
        blank=True,
        validators=[RegexValidator(r"^\+?[1-9]\d{1,14}$", "Use o formato E.164, ex.: +5511999999999.")],
    )

    data_nascimento = models.DateField("Data de nascimento", null=True, blank=True)
    sexo = models.CharField("Sexo", max_length=1, choices=Sexo.choices, blank=True)

    # Endereço (campos opcionais)
    logradouro = models.CharField("Logradouro", max_length=120, blank=True)
    numero = models.CharField("Número", max_length=10, blank=True)
    complemento = models.CharField("Complemento", max_length=60, blank=True)
    bairro = models.CharField("Bairro", max_length=60, blank=True)
    cidade = models.CharField("Cidade", max_length=60, blank=True)
    uf = models.CharField("UF", max_length=2, blank=True)
    cep = models.CharField(
        "CEP",
        max_length=8,
        blank=True,
        validators=[RegexValidator(r"^\d{8}$", "Informe 8 dígitos, somente números.")],
        help_text="Apenas números (ex.: 69900970).",
    )

    ativo = models.BooleanField("Ativo", default=True)

    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"
        indexes = [
            models.Index(fields=["cpf"]),
            models.Index(fields=["nome"]),
        ]

    def __str__(self):
        return self.nome

    @property
    def idade(self):
        """Idade em anos (ou None se sem data de nascimento)."""
        if not self.data_nascimento:
            return None
        hoje = date.today()
        return (
            hoje.year
            - self.data_nascimento.year
            - ((hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day))
        )

    def save(self, *args, **kwargs):
        # Normaliza campos: mantém apenas dígitos e padroniza UF em maiúsculas
        if self.cpf:
            self.cpf = re.sub(r"\D", "", self.cpf)
        if self.cep:
            self.cep = re.sub(r"\D", "", self.cep)
        if self.uf:
            self.uf = self.uf.upper()
        super().save(*args, **kwargs)
