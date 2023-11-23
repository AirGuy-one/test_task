from rest_framework.test import APITestCase


class CDRTests(APITestCase):
    def test_get_cdr_list(self):
        response = self.client.get('/cdr/')
        self.assertEqual(response.status_code, 200)
