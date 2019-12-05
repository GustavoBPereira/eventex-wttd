from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core import mail
from django.template.loader import render_to_string

from eventex.subscriptions.forms import subscriptionForm
from eventex.subscriptions.models import Subscription

def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)        


def create(request):
    form = subscriptionForm(request.POST)
    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html', {'form': form})

    subscription = Subscription.objects.create(**form.cleaned_data)

    _send_email('Confirmação de inscrição',
                settings.DEFAULT_FROM_EMAIL,
                subscription.email,
                'subscriptions/subscription_email.txt',
                {'subscription': subscription})

    messages.success(request, 'Inscrição realizada com sucesso!')
    
    return HttpResponseRedirect(f'/inscricao/{subscription.pk}/')


def detail(request, pk):
    try:
        subscription = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        raise Http404

    return render(request, 'subscriptions/subscription_detail.html',
                    {'subscription': subscription})


def new(request):
    return render(request, 'subscriptions/subscription_form.html',
                {'form': subscriptionForm()})


def _send_email(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])