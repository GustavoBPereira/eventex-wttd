from django.db import models
from django.shortcuts import resolve_url as r
from eventex.subscriptions.validators import validate_cpf


class Subscription(models.Model):
    name = models.CharField('Nome', max_length=100)
    cpf = models.CharField('CPF', max_length=11, validators=[validate_cpf])
    email = models.EmailField('E-mail', blank=True)
    phone = models.CharField('Telefone', max_length=20, blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    paid = models.BooleanField('Pago', default=False)

    class Meta:
        verbose_name_plural = 'inscrições'
        verbose_name = 'inscrição'
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return r('subscriptions:detail', self.pk)

    def __str__(self):
        return self.name
