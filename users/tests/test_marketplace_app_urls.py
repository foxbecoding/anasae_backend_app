from django.test import SimpleTestCase
from django.urls import reverse, resolve

class TestMAUserUrls(SimpleTestCase):

    def test_ma_user_detail_url_resolves(self):
        url = reverse('ma-user-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).view_name, 'ma-user-detail')