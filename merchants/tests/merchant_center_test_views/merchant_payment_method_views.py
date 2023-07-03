from django.test import TestCase, Client
from django.urls import reverse
from merchants.models import *
from users.models import UserGender
from datetime import datetime
import stripe

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

        setup_intent_create_res = stripe.SetupIntent.create(
            customer=self.user['stripe_customer_id'],
            payment_method="pm_card_visa"
        )
        
        self.setup_intent_confirm_res = stripe.SetupIntent.confirm(
            setup_intent_create_res.id,
            payment_method="pm_card_visa"
        )

    def test_mc_merchant_payment_method_get_client_secret_list(self):
        res = self.client.get(reverse('mc-merchant-payment-method-list'))
        self.assertEqual(res.status_code, 200)
        
    def test_mc_merchant_payment_method_create(self):
        res = self.client.post(
            reverse('mc-merchant-payment-method-list'),
            data = {'payment_method_id': self.setup_intent_confirm_res.payment_method},
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        
        self.assertGreater(len(res.data['payment_methods']), 0)
        self.assertEqual(res.status_code, 201)
    
    def test_mc_merchant_payment_method_destroy(self):
        create_res = self.client.post(
            reverse('mc-merchant-payment-method-list'),
            data = {'payment_method_id': self.setup_intent_confirm_res.payment_method},
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        delete_res = self.client.delete(
            reverse(
                'mc-merchant-payment-method-detail',
                kwargs={'pk': create_res.data['payment_methods'][0]['pk']}
            ),
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.assertEqual(len(delete_res.data['payment_methods']), 0)
        self.assertEqual(delete_res.status_code, 202)

    def test_mc_merchant_payment_method_destroy_permissions_failed(self):
        self.client.post(
            reverse('mc-merchant-payment-method-list'),
            data = {'payment_method_id': self.setup_intent_confirm_res.payment_method},
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        delete_res = self.client.delete(
            reverse(
                'mc-merchant-payment-method-detail',
                kwargs={'pk': 18}
            ),
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.assertEqual(delete_res.status_code, 403)
