from django.shortcuts import render
from eventex.subscriptions.forms import subscriptionForm

def subscribe(request):
    context = {'form': subscriptionForm()}
    return render(request, 'subscriptions/subscription_form.html', context)
# Create your views here.