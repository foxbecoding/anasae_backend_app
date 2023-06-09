from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from datetime import datetime


class TestUsersViews(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.list_url = reverse('user-sign-up-list')
        date_time_str = '12/31/1990'
        self.date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y')

        self.user = User.objects.create(
            first_name = "Desmond",
            last_name = 'Fox',
            email = 'fox@foxbecoding.com',
            date_of_birth = self.date_time_obj.date(),
            agreed_to_toa = True
        )
        # self.user.save()
        # self.detail_url = reverse('user-detail', kwargs={'pk': self.user.id})

    # create()
    def test_users_create(self):
        #set user data
        user = {
            'first_name': "Desmond",
            'last_name': 'Fox',
            'email': 'fox@foxbecoding.com',
            'password': '123456',
            'confirm_password': '123456',
            'date_of_birth': self.date_time_obj.date(),
            'agreed_to_toa': True
        }
    
        #Get user data from response
        res = self.client.post(self.list_url, user)

        #check if data is correct
        self.assertEquals(res.data['first_name'], 'Desmond')
        self.assertEquals(res.status_code, 201)
    
    def test_users_create_no_data(self):
        #set user data
        user = {}

        #Get user data from response
        res = self.client.post(self.list_url, user)

        #check if data is correct
        self.assertEquals(res.status_code, 400)

#     # list()
#     def test_users_list(self):
#         res = self.client.get(self.list_url)

#         self.assertGreater(len(res.data), 0)
#         self.assertEquals(res.status_code, 200)
    
#     # retrieve()
#     def test_users_retrieve(self):
#         res = self.client.get(self.detail_url)

#         self.assertEquals(res.status_code, 200)
#         self.assertEquals(res.data['pk'], self.user.id)
    
#     def test_users_retrieve_404_Not_Found(self):
#         user = User.objects.create(
#             wallet = '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfBa',
#             real_wallet = '1A1zP1eP5QGefi2DMPTfTL5SLMV7DivfBa',
#             email = 'foxxx@easybeatz.com',
#             username = 'FOxxX',
#         )
#         user.save()
#         detail_url = reverse('user-detail', kwargs={'pk': 1000})
        
#         res = self.client.get(detail_url)
        
#         self.assertEquals(res.status_code, 404)
#         self.assertEquals(res.data, None)

# class TestUserWalletConnectsViews(TestCase):
    
#     def setUp(self):
#         self.client = Client()
#         self.list_url = reverse('user-wallet-connect-list')
#         self.user = User.objects.create(
#             wallet = '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
#             real_wallet = '1A1zP1eP5QGefi2DMPTfTL5SLMV7DivfNa',
#             email = 'fox@easybeatz.com',
#             username = 'FOX',
#         )
#         self.user.save()
#         Token.objects.create(user=self.user)
#         self.user_wallet_connect = UserWalletConnect.objects.create(
#             user = self.user
#         )
#         self.user_wallet_connect.save()

#         # self.detail_url = reverse('user-wallet-connect-detail', kwargs={'pk': self.user_wallet_connect.id})

#     # list()
#     def test_user_wallet_connects_list(self):
#         res = self.client.get(self.list_url)

#         self.assertGreater(len(res.data), 0)
#         self.assertEquals(res.status_code, 200)

#     # create()
#     def test_user_wallet_connects_create(self):
#         user_data = {
#             'wallet': self.user.wallet,
#             'real_wallet': self.user.real_wallet
#         }
#         res = self.client.post(self.list_url, user_data)

#         self.assertEquals(user_data['wallet'], res.data['data']['wallet'])
#         self.assertEquals(res.status_code, 201)
    
#     def test_user_wallet_connects_create_user_not_found(self):
#         user_data = {
#             'wallet': 'ds',
#             'real_wallet': 'dsd'
#         }
#         res = self.client.post(self.list_url, user_data)

#         self.assertEquals(res.status_code, 404)
    
#     def test_user_wallet_connects_create_no_wallet(self):
#         user_data = {
#             'real_wallet': self.user.real_wallet
#         }
#         res = self.client.post(self.list_url, user_data)

#         self.assertEquals(res.status_code, 400)
    
#     def test_user_wallet_connects_create_no_real_wallet(self):
#         user_data = {
#             'wallet': self.user.wallet,
#         }
#         res = self.client.post(self.list_url, user_data)

#         self.assertEquals(res.status_code, 400)