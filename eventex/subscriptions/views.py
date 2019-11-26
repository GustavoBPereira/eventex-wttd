from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core import mail
from django.template.loader import render_to_string

from eventex.subscriptions.forms import subscriptionForm

def subscribe(request):
    if request.method == 'POST':
        form = subscriptionForm(request.POST)
        if form.is_valid():
            body = render_to_string('subscriptions/subscription_email.txt', form.cleaned_data)
            mail.send_mail('Confirmação de inscrição',
                            body,
                            'contato@eventex.com',
                            ['contato@eventex.com', form.cleaned_data['email']])
            messages.success(request, 'Inscrição realizada com sucesso!')
            
            return HttpResponseRedirect('/inscricao/')
        else:
            return render(request, 'subscriptions/subscription_form.html', {'form': form})
    else:
        context = {'form': subscriptionForm()}
        return render(request, 'subscriptions/subscription_form.html', context)
# Create your views here.