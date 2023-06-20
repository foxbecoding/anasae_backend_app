from django.test import TestCase, Client
from django.urls import reverse
from merchants.models import *
from utils.helpers import create_uid
from pprint import pprint

class TestMCMerchantViewSet(TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_mc_merchant_list(self):
        # res = self.client.get(reverse('mc-merchant-list'))
        # self.assertEqual(res.status_code, 200)