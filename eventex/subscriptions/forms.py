from django import forms
from django.core.exceptions import ValidationError

from eventex.subscriptions.models import Subscription
from eventex.subscriptions.validators import validate_cpf


class subscriptionFormOld(forms.Form):
    name = forms.CharField(label="Nome")
    cpf = forms.CharField(label="CPF", validators=[validate_cpf])
    email = forms.EmailField(label="Email", required=False)
    phone = forms.CharField(label="Telefone", required=False)

    def clean_name(self):
        name = self.cleaned_data['name']
        return name.title()

    def clean(self):
        if not self.cleaned_data.get('email') and not self.cleaned_data.get('phone'):
            raise ValidationError('Informe o seu email ou telefone')

        return self.cleaned_data


class SubscriptionForm(forms.ModelForm):
    cpf = forms.CharField(label="CPF", validators=[validate_cpf])

    class Meta:
        model = Subscription
        fields = ['name', 'cpf', 'email', 'phone']

    def clean_name(self):
        name = self.cleaned_data['name']
        return name.title()

    def clean(self):
        self.cleaned_data = super().clean()

        if not self.cleaned_data.get('email') and not self.cleaned_data.get('phone'):
            raise ValidationError('Informe o seu email ou telefone')

        return self.cleaned_data
