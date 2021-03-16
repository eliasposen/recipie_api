from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Tests the users API (public)"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Tests creating user with valid payload works"""
        payload = {
            'email': 'test@elias.com', 'password': 'billyboy', 'name': 'Ed'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_duplicate_user(self):
        """Tests creating a user that already exists fails"""
        payload = {
            'email': 'test@elias.com', 'password': 'billyboy', 'name': 'Ed'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_short(self):
        """Tests password must be more than 5 characters"""
        payload = {'email': 'test@elias.com', 'password': 'pw', 'name': 'Ed'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Tests token is created for a valid user"""
        payload = {
            'email': 'test@elias.com', 'password': 'billyboy', 'name': 'Ed'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_creds(self):
        """Tests token is not created when given invalid credentials"""
        create_user(email='test@elias.com', password='testpass')
        payload = {
            'email': 'test@elias.com', 'password': 'wrong!', 'name': 'Ed'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Tests that the token is not created if the user does not exist"""
        payload = {
            'email': 'test@elias.com', 'password': 'billyboy', 'name': 'Ed'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def tess_create_token_missing_password(self):
        """Tests that email and password are required"""
        res = self.client.post(
            TOKEN_URL,
            {'email': 'test@elias.com', 'password': '', 'name': 'Ed'},
        )

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
