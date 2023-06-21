from django.test import SimpleTestCase
from django.urls import reverse, resolve

class TestMCMerchantUrls(SimpleTestCase):

    def test_mc_merchant_list_url_resolves(self):
        url = reverse('mc-merchant-list')
        self.assertEqual(resolve(url).view_name, 'mc-merchant-list')
    
    def test_mc_merchant_detail_url_resolves(self):
        url = reverse('mc-merchant-detail', kwargs={'uid': 'm-IH4io44f'})
        self.assertEqual(resolve(url).view_name, 'mc-merchant-detail')

class TestMCMerchantSubscriptionUrls(SimpleTestCase):

    def test_mc_merchant_subscription_list_url_resolves(self):
        url = reverse('mc-merchant-subscription-list')
        self.assertEqual(resolve(url).view_name, 'mc-merchant-subscription-list')
    
    def test_mc_merchant_subscription_detail_url_resolves(self):
        url = reverse('mc-merchant-subscription-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).view_name, 'mc-merchant-subscription-detail')