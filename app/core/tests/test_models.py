from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Tests creating new user with email is successful"""
        email = 'test@eliasposen.com'
        password = "testme123"
        user = get_user_model().objects.create_user(
            email=email, password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalised(self):
        """Tests the email is normalised for new user"""
        email = 'test@ELIASPOSEN.com'
        user = get_user_model().objects.create_user(
            email, 'testing'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Tests creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testing')

    def test_create_new_superuser(self):
        """Tests creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@eliasposen.com', 'test123'
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
