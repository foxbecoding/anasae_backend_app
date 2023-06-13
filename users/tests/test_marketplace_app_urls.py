from django.test import SimpleTestCase
from django.urls import reverse, resolve

class TestMAUserUrls(SimpleTestCase):

    def test_mpa_user_detail_url_resolves(self):
        url = reverse('mpa-user-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).view_name, 'mpa-user-detail')

class TestMAUserProfileUrls(SimpleTestCase):

    def test_mpa_user_profile_list_url_resolves(self):
        url = reverse('mpa-user-profile-list')
        self.assertEqual(resolve(url).view_name, 'mpa-user-profile-list')
    
    def test_mpa_user_profile_detail_url_resolves(self):
        url = reverse('mpa-user-profile-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).view_name, 'mpa-user-profile-detail')