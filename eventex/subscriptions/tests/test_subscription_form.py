from django.test import TestCase
from eventex.subscriptions.forms import subscriptionForm

class SubscriptionFormTest(TestCase):
    def setUp(self):
        self.form = subscriptionForm()

    def test_form_has_fields(self):
        expected = ['name', 'cpf', 'email', 'phone']
        self.assertSequenceEqual(expected, list(self.form.fields))