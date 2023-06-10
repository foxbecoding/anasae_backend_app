from django.test import SimpleTestCase
from django.urls import reverse, resolve

class TestUserSignUpUrls(SimpleTestCase):
    
    def test_user_sign_up_list_url_resolves(self):
        url = reverse('user-sign-up-list')
        self.assertEqual(resolve(url).view_name, 'user-sign-up-list')

    # def test_user_sign_up_detail_url_resolves(self):
    #     url = reverse('user-sign-up-detail', kwargs={'pk': 1})
    #     self.assertEqual(resolve(url).view_name, 'user-sign-up-detail')

class TestUserLogInUrls(SimpleTestCase):
    
    def test_user_log_in_list_url_resolves(self):
        url = reverse('user-log-in-list')
        self.assertEqual(resolve(url).view_name, 'user-log-in-list')

class TestUserLogOutUrls(SimpleTestCase):
    
    def test_user_log_out_list_url_resolves(self):
        url = reverse('user-log-out-list')
        self.assertEqual(resolve(url).view_name, 'user-log-out-list')