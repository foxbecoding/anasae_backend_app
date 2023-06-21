from django.test import TestCase, Client
from django.urls import reverse
from merchants.models import *
from users.models import UserGender
from pprint import pprint
from datetime import datetime

class TestMCMerchantViewSet(TestCase):
    
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        date_time_str = '12/31/1990'
        self.date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y')
        self.client.get(reverse('x-fct-list'))
        self.csrftoken = self.client.cookies['csrftoken'].value
        self.user_gender = UserGender.objects.create(gender = 'male')
        self.user_gender.save()

        #User Sign up
        user_sign_up_data = {
            'first_name': "Desmond",
            'last_name': 'Fox',
            'email': 'fox@foxbecoding.com',
            'password': '123456',
            'confirm_password': '123456',
            'date_of_birth': self.date_time_obj.date(),
            'agreed_to_toa': True,
            'gender': self.user_gender.pk
        }

        self.client.post(
            reverse('account-sign-up-list'), 
            user_sign_up_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        #User Login
        login_credentials = {
            'email': 'fox@foxbecoding.com',
            'password': '123456'
        }
    
        #Get response data
        res = self.client.post(
            reverse('account-log-in-list'), 
            login_credentials, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.user = res.data
        self.csrftoken = self.client.cookies['csrftoken'].value

    def test_mc_merchant_create(self):
        res = self.client.post(
            reverse('mc-merchant-list'),
            data = {'title': 'Fenty Beauty'},
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.assertEqual(res.data['title'], 'Fenty Beauty')
        self.assertEqual(res.status_code, 201)
    
    def test_mc_merchant_create_error(self):
        res = self.client.post(
            reverse('mc-merchant-list'),
            data = {},
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.assertEqual(res.status_code, 400)

class TestMCMerchantSubscriptionViewSet(TestCase):
    
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        date_time_str = '12/31/1990'
        self.date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y')
        self.client.get(reverse('x-fct-list'))
        self.csrftoken = self.client.cookies['csrftoken'].value
        self.user_gender = UserGender.objects.create(gender = 'male')
        self.user_gender.save()

        #User Sign up
        user_sign_up_data = {
            'first_name': "Desmond",
            'last_name': 'Fox',
            'email': 'fox@foxbecoding.com',
            'password': '123456',
            'confirm_password': '123456',
            'date_of_birth': self.date_time_obj.date(),
            'agreed_to_toa': True,
            'gender': self.user_gender.pk
        }

        self.client.post(
            reverse('account-sign-up-list'), 
            user_sign_up_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        #User Login
        login_credentials = {
            'email': 'fox@foxbecoding.com',
            'password': '123456'
        }
    
        #Get response data
        res = self.client.post(
            reverse('account-log-in-list'), 
            login_credentials, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.user = res.data
        self.csrftoken = self.client.cookies['csrftoken'].value

        # Create Merchants plans, prices and features
        merchant_plans = [
            {'title': 'Basic', 'description': '', 'product_listings': 5, 'is_active': True},
            {'title': 'Pro', 'description': '', 'product_listings': 20, 'is_active': True},
            {'title': 'Plus', 'description': '', 'product_listings': 50, 'is_active': True}
        ]
        Merchant_Plan_Instances = []
        for plan in merchant_plans:
            Merchant_Plan_Instance = MerchantPlan.objects.create(
                title = plan['title'],
                description = plan['description'],
                product_listings = plan['product_listings'],
                is_active = plan['is_active']
            )
            Merchant_Plan_Instance.save()
            Merchant_Plan_Instances.append(Merchant_Plan_Instance)
        
        merchant_plan_prices = [
            {'title': 'Free', 'description': '', 'price': 0},
            {'title': '$9.99', 'description': '', 'price': 999},
            {'title': '$19.99', 'description': '', 'price': 1999}
        ]
        merchant_plan_prices
        for plan_price in merchant_plan_prices:
            MerchantPlanPrice.objects.create(
                merchant_plan = models.ForeignKey(MerchantPlan, on_delete=models.CASCADE, related_name="plan_prices")
                title = models.CharField(max_length=200, blank=False)
                description = models.CharField(max_length=2000, blank=True, null=True)
                price = models.FloatField(blank=False)
                stripe_price_key = models.CharField(max_length=200, blank=False)
                is_active = models.BooleanField(default=False)
            ) 

    def test_mc_merchant_subscription_create(self):
        pass