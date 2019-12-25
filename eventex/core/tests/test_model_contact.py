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
