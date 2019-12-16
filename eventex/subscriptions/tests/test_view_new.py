from django.test import TestCase
from django.core import mail
from django.shortcuts import resolve_url as r

from eventex.subscriptions.forms import subscriptionForm
from eventex.subscriptions.models import Subscription


class subscriptionsNewGet(TestCase):
    def setUp(self):
        self.response = self.client.get(r('subscriptions:new'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_html(self):
        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"', 1)
                )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoke')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, subscriptionForm)


class subscriptionsNewPostValid(TestCase):
    def setUp(self):
        data = dict(name='Gustavo Brito', cpf='12345678901',
                    email='britopereiragustavo@gmail.com', phone='21-99358-7250')
        self.resp = self.client.post(r('subscriptions:new'), data)

    def test_post(self):
        self.assertRedirects(self.resp, r('subscriptions:detail', 1))
        self.assertEqual(302, self.resp.status_code)

    def test_send_subscribe_mail(self):
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())


class subscriptionsNewPostInvalid(TestCase):
    def setUp(self):
        self.resp = self.client.post(r('subscriptions:new'), {})

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

    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())

class TemplateRegressionTest(TestCase):
    def test_template_has_non_fields_errors(self):
        invalid_data = dict(name='Gustavo Brito', cpf='12345678901')
        response = self.client.post(r('subscriptions:new'), invalid_data)

        self.assertContains(response, '<ul class="errorlist nonfield"')
