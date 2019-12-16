from django.test import TestCase
from eventex.subscriptions.forms import subscriptionForm


class SubscriptionFormTest(TestCase):
    def test_form_has_fields(self):
        form = subscriptionForm()
        expected = ['name', 'cpf', 'email', 'phone']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_cpf_is_digits(self):
        form = self.make_validated_form(cpf='abcd5678901')
        field = 'cpf'
        msg = 'digits'
        self.assertFormErrorCode(form, 'cpf', 'digits')
        # self.assertFormErrorMessage(form, field, msg)

    def test_cpf_has_11_digits(self):
        form = self.make_validated_form(cpf='1234')
        self.assertFormErrorCode(form, 'cpf', 'length')

    def test_name_must_be_capitalized(self):
        form = self.make_validated_form(name='GUSTAVO brito')
        self.assertEqual('Gustavo Brito', form.cleaned_data['name'])

    def make_validated_form(self, **kwargs):
        valid = dict(name='Gustavo Brito', cpf='12345678901',
                     email='britopereiragustavo@gmail.com', phone='21-993587250')
        data = dict(valid, **kwargs)
        form = subscriptionForm(data)
        form.is_valid()
        return form

    def test_email_is_optional(self):
        form = self.make_validated_form(email='')
        self.assertFalse(form.errors)

    def test_phone_is_optional(self):
        form = self.make_validated_form(phone='')
        self.assertFalse(form.errors)

    def test_must_have_email_or_phone(self):
        form = self.make_validated_form(email='',phone='')
        self.assertListEqual(['__all__'], list(form.errors))

    def assertFormErrorMessage(self, form, field, msg):
        errors = form.errors
        errors_list = errors[field]
        self.assertListEqual([msg], errors_list)

    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        errors_list = errors[field]
        exception = errors_list[0]
        self.assertEqual(code, exception.code)