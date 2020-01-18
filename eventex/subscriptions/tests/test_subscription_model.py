from datetime import datetime
from django.shortcuts import resolve_url as r
from django.test import TestCase
from eventex.subscriptions.models import Subscription

class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name = 'Gustavo Brito',
            cpf= '12345678901',
            email= 'britopereiragustavo@gmail.com',
            phone='21-99358-7250'
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())
    
    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)
    
    def test_str(self):
        self.assertEqual('Gustavo Brito', str(self.obj))
    
    def test_paid_default_to_false(self):
        self.assertEqual(False, self.obj.paid)

    def test_get_absolute_url(self):
        url = r('subscriptions:detail', self.obj.pk)
        self.assertEqual(url, self.obj.get_absolute_url())