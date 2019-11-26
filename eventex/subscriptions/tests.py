from django.test import TestCase
from django.core import mail
from eventex.subscriptions.forms import subscriptionForm

class subscribeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/')
    
    def test_get(self):
        self.assertEqual(200, self.response.status_code)
    
    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')
    
    def test_html(self):
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')
    
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoke')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, subscriptionForm)
    
    def test_form_has_fields(self):
        form = self.response.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))

class subscribePostTest(TestCase):
    def setUp(self):
        data = dict(name = 'Gustavo Brito', cpf= '12345678901',
                    email= 'britopereiragustavo@gmail.com', phone='21-99358-7250')
        self.resp = self.client.post('/inscricao/', data)
    
    def test_post(self):
        self.assertEqual(302, self.resp.status_code)
    
    def test_send_subscribe_mail(self):
        self.assertEqual(1, len(mail.outbox))
    
    def test_subscription_mail_subject(self):
        email = mail.outbox[0]
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, email.subject)
    
    def test_subscription_mail_from(self):
        email = mail.outbox[0]
        expect = 'contato@eventex.com'
        self.assertEqual(expect, email.from_email)
    
    def test_subscription_mail_to(self):
        email = mail.outbox[0]
        expect = ['contato@eventex.com', 'britopereiragustavo@gmail.com']

        self.assertEqual(expect, email.to)

    def test_subscription_mail_body(self):
        email = mail.outbox[0]
        self.assertIn('Gustavo Brito', email.body)
        self.assertIn('12345678901', email.body)
        self.assertIn('britopereiragustavo@gmail.com', email.body)
        self.assertIn('21-99358-7250', email.body)

class subscribeInvalidPost(TestCase):
    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})

    def test_post(self):
        self.assertEqual(200, self.resp.status_code)
    
    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')
    
    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, subscriptionForm)
    
    def test_form_has_erros(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

class subscribeSucessMessage(TestCase):
    def test_message(self):
        data = dict(name = 'Gustavo Brito', cpf= '12345678901',
                    email= 'britopereiragustavo@gmail.com', phone='21-99358-7250')
        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, 'Inscrição realizada com sucesso!')