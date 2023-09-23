from django.test import TestCase
from django.contrib.auth.models import User

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from restaurant.models import Menu
from restaurant.serializers import MenuSerializer


class MenuViewTest(TestCase):

    def setUp(self):

        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpwd,'
        )
        self.item1 = Menu.objects.create(
            title="Pizza", price=14, inventory=5)
        self.item2 = Menu.objects.create(
            title="Burger", price=8.99, inventory=10)

    def testUserLogin(self):

        self.client.login(username='testuser', password='testpwd')
        user = User.objects.get(username='testuser')
        self.client.force_authenticate(user=user)

    def test_auth(self):

        response = self.client.get(reverse('menu-view'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.testUserLogin()
        response = self.client.get(reverse('menu-view'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_getall(self):

        self.testUserLogin()
        response = self.client.get(reverse('menu-view'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        menu_items = Menu.objects.all()
        serializer = MenuSerializer(menu_items, many=True)
        self.assertEqual(response.data, serializer.data)
