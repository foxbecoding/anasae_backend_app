from django.test import TestCase, Client
from django.urls import reverse
from merchants.models import *
from users.models import UserGender
from datetime import datetime

class TestMCMerchantPlanViewSet(TestCase):
    
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
        self.client.post(
            reverse('account-log-in-list'), 
            login_credentials, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        # Create Merchants plans, prices and features
        merchant_plans = (
            {'title': 'Basic', 'description': '', 'product_listings': 5, 'is_active': True},
            {'title': 'Pro', 'description': '', 'product_listings': 20, 'is_active': True},
            {'title': 'Plus', 'description': '', 'product_listings': 50, 'is_active': True}
        )
        
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
        
        merchant_plan_prices = (
            {
                'title': 'Free', 
                'description': '', 
                'stripe_price_key': 'price_1NLUImIXJRFgDdeh0yyCtHUQ', 
                'price': 000, 
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

        merchant_plan_prices = zip(merchant_plan_prices, Merchant_Plan_Instances)
        Merchant_Plan_Prices_Instances = []
        
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
            Merchant_Plan_Prices_Instances.append(Merchant_Plan_Prices_Instance)

        merchant_plan_features = [
            ['5 product listings', 'Product analytics', 'Sales analytics'],
            ['20 product listings', 'Product analytics', 'Sales analytics'],
            ['50 product listings', 'Product analytics', 'Sales analytics'],
        ]

        merchant_plan_features = zip(merchant_plan_features, Merchant_Plan_Instances)
        self.Merchant_Plan_Features_Instances = []
        
        for plan_feature in merchant_plan_features:
            features = plan_feature[0]
            merchant_plan = plan_feature[1]

            for feature in features:
                Merchant_Plan_Feature_Instance = MerchantPlanFeature.objects.create(
                    merchant_plan = merchant_plan,
                    title = feature
                )
                Merchant_Plan_Feature_Instance.save()


    def test_mc_merchant_plan_list(self):
        res = self.client.get(reverse('mc-merchant-plan-list'))
        self.assertEqual(res.status_code, 200)