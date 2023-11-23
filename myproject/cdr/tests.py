from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from .models import CallDetailRecord
from uuid import UUID


class CDRListCreateViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_create_url = reverse('cdr-list')
        self.detail_url = reverse('cdr-detail', kwargs={'pk': UUID('550e8400-e29b-41d4-a716-446655450000')})
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = self.create_user()
        self.access_token = self.obtain_access_token()

    def create_user(self):
        return User.objects.create_user(username=self.username, password=self.password)

    def obtain_access_token(self):
        response = self.client.post(reverse('token_obtain_pair'),
                                    {'username': self.username, 'password': self.password}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def test_authenticated_create_request(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        data = {
            'cdr_data': [
                {
                    "call_id": "550e8400-e29b-41d4-a716-446655420000",
                    "caller_number": "+79998887763",
                    "callee_number": "+79874561213",
                    "start_time": "2023-11-24T17:15:00Z",
                    "end_time": "2023-11-24T17:20:00Z",
                    "duration": "00:05:00",
                    "call_type": "outgoing",
                    "call_status": "successful",
                },
            ]
        }

        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
