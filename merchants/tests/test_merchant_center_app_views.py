from django.test import TestCase, Client
from django.urls import reverse
from merchants.models import *
from users.models import UserGender
from pprint import pprint
from datetime import datetime
import stripe

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

    def test_mc_merchant_retrieve(self):
        create_merchant_res = self.client.post(
            reverse('mc-merchant-list'),
            data = {'title': 'Fenty Beauty'},
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        merchant_uid = create_merchant_res.data['uid']
        res = self.client.get(
            reverse('mc-merchant-detail', kwargs={ 'uid': merchant_uid })
        )
        self.assertEqual(res.data['title'], 'Fenty Beauty')
        self.assertEqual(res.status_code, 200)
    
    def test_mc_merchant_retrieve_permissions_failed(self):
        self.client.post(
            reverse('mc-merchant-list'),
            data = {'title': 'Fenty Beauty'},
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        res = self.client.get(
            reverse('mc-merchant-detail', kwargs={ 'uid': 'merchant_uid' })
        )
        self.assertEqual(res.status_code, 403)

class TestMCMerchantPaymentMethodViewSet(TestCase):

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

        # Create Merchant Account
        self.merchant_res = self.client.post(
            reverse('mc-merchant-list'),
            data = {'title': 'Fenty Beauty'},
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

    def test_mc_merchant_payment_method_get_client_secret_list(self):
        res = self.client.get(reverse('mc-merchant-payment-method-list'))
        self.assertEqual(res.status_code, 200)
        
    def test_mc_merchant_payment_method_create(self):
        setup_intent_create_res = stripe.SetupIntent.create(
            customer=self.user['stripe_customer_id'],
            payment_method="pm_card_visa"
        )
        
        setup_intent_confirm_res = stripe.SetupIntent.confirm(
            setup_intent_create_res,
            payment_method="pm_card_visa",
        )
        
        res = self.client.post(
            reverse('mc-merchant-payment-method-list'),
            data = {'intent_id': setup_intent_confirm_res.payment_method},
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        # self.assertEqual(res.status_code, 201)


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

        # Create Merchant Account
        self.merchant_res = self.client.post(
            reverse('mc-merchant-list'),
            data = {'title': 'Fenty Beauty'},
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        # Create Merchants plans, prices and features
        merchant_plans = (
            {'title': 'Basic', 'description': '', 'product_listings': 5, 'is_active': True},
            {'title': 'Pro', 'description': '', 'product_listings': 20, 'is_active': True},
            {'title': 'Plus', 'description': '', 'product_listings': 50, 'is_active': True}
        )
        self.Merchant_Plan_Instances = []
        for plan in merchant_plans:
            Merchant_Plan_Instance = MerchantPlan.objects.create(
                title = plan['title'],
                description = plan['description'],
                product_listings = plan['product_listings'],
                is_active = plan['is_active']
            )
            Merchant_Plan_Instance.save()
            self.Merchant_Plan_Instances.append(Merchant_Plan_Instance)
        
        merchant_plan_prices = (
            {
                'title': 'Free', 
                'description': '', 
                'stripe_price_key': 'price_1NLUImIXJRFgDdeh0yyCtHUQ', 
                'price': 0, 
                'is_active': True
            },
            {
                'title': '$9.99', 
                'description': '', 
                'stripe_price_key': 'price_1NLUKWIXJRFgDdehiEcufcrB',
                'price': 999,
                'is_active': True
            },
            {
                'title': '$19.99', 
                'description': '',
                'stripe_price_key': 'price_1NLVCYIXJRFgDdehvHzX0w4o', 
                'price': 1999,
                'is_active': True
            }
        )
        merchant_plan_prices = zip(merchant_plan_prices, self.Merchant_Plan_Instances)
        self.Merchant_Plan_Prices_Instances = []
        for plan_price in merchant_plan_prices:
            data = plan_price[0]
            merchant_plan = plan_price[1]
            Merchant_Plan_Prices_Instance = MerchantPlanPrice.objects.create(
                merchant_plan = merchant_plan,
                title = data['title'],
                description = data['description'],
                price = data['price'],
                stripe_price_key = data['stripe_price_key'],
                is_active = data['is_active']
            ) 
            Merchant_Plan_Prices_Instance.save()
            self.Merchant_Plan_Prices_Instances.append(Merchant_Plan_Prices_Instance)

    def test_mc_merchant_subscription_create(self):
        res = self.client.post(
            reverse('mc-merchant-subscription-list'),
            data = {},
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.assertEqual(res.status_code, 201)

    # def test_mc_merchant_subscription_retrieve(self):
    #     res = self.client.get(
    #         reverse(
    #             'mc-merchant-subscription-detail', 
    #             kwargs={'pk': self.merchant_res.data['pk']}
    #         ),
    #         data = {},
    #         **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #     )
    #     pass