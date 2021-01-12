from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self) -> None:
        """Generates data for test cases"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='elias@posen.com',
            password='passwordIsSecure',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@posen.com',
            password='blahblah',
            name='Test user full name'
        )

    def test_users_listed(self):
        """Tests users are listed on user page of admin panel"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Tests that the user edit page functions"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Tests create user page functions"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
