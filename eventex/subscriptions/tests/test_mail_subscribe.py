from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r

class subscribePostValidContent(TestCase):
    def setUp(self):
        data = dict(name = 'Gustavo Brito', cpf= '12345678901',
                    email= 'britopereiragustavo@gmail.com', phone='21-99358-7250')
        self.client.post(r('subscriptions:new'), data)
        self.email = mail.outbox[0]
    
    def test_subscription_mail_subject(self):
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, self.email.subject)
    
    def test_subscription_mail_from(self):
        expect = 'contato@eventex.com'
        self.assertEqual(expect, self.email.from_email)
    
    def test_subscription_mail_to(self):
        expect = ['contato@eventex.com', 'britopereiragustavo@gmail.com']

        self.assertEqual(expect, self.email.to)

    def test_subscription_mail_body(self):

        contents = (('Gustavo Brito'),
                    ('12345678901'),
                    ('britopereiragustavo@gmail.com'),
                    ('21-99358-7250')
                    )
        for content in contents:
            self.assertIn(content, self.email.body)
