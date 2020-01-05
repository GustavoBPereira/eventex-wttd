from django.core.exceptions import ValidationError
from django.test import TestCase
from eventex.core.models import Speaker, Contact


class ContactModelTest(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(
            name='Gustavo Brito',
            slug='gustavo-brito',
            photo='http://hbn.link/turing-pic'
        )

    def test_email(self):
        contact = Contact.objects.create(
            speaker=self.speaker,
            kind=Contact.EMAIL,
            value='britopereiragustavo@gmail.com'
        )
        self.assertTrue(Contact.objects.exists())

    def test_phone(self):
        contact = Contact.objects.create(
            speaker=self.speaker,
            kind=Contact.PHONE,
            value='21-993587250'
        )
        self.assertTrue(Contact.objects.exists())

    def test_choices(self):
        """Contact kind must be limited to E or P"""
        contact = Contact(
            self.speaker,
            kind='A',
            value='B'
        )
        self.assertRaises(ValidationError, contact.full_clean)

    def test_str(self):
        contact = Contact(
            speaker=self.speaker,
            kind=Contact.EMAIL,
            value='britopereiragustavo@gmail.com'
        )
        self.assertEqual('britopereiragustavo@gmail.com', str(contact))


class ContactManagerTest(TestCase):
    def setUp(self):
        s = Speaker.objects.create(
            name='Henrrique Bastos',
            slug='henrrique-bastos',
            photo='http://hbn.link/hb-pic'
        )
        s.contact_set.create(kind=Contact.EMAIL, value='henrique@bastos.net')
        s.contact_set.create(kind=Contact.PHONE, value='21-9961866180')

    def test_emails(self):
        qs = Contact.objects.emails()
        expected = ['henrique@bastos.net']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)

    def test_phones(self):
        qs = Contact.objects.phones()
        expected = ['21-9961866180']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)
