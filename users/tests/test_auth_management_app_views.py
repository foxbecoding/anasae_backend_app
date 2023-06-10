from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from django.middleware.csrf import get_token
from users.models import User, UserLogin
from datetime import datetime


class TestUserSignUpViewSet(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.list_url = reverse('user-sign-up-list')

    def test_user_sign_up_create(self):
        #set user data
        date_time_str = '12/31/1990'
        date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y')
        
        request_data = {
            'first_name': "Desmond",
            'last_name': 'Fox',
            'email': 'fox@foxbecoding.com',
            'password': '123456',
            'confirm_password': '123456',
            'date_of_birth': date_time_obj.date(),
            'agreed_to_toa': True
        }
    
        #Get user data from response
        res = self.client.post(self.list_url, request_data)

        #check if data is correct
        self.assertEquals(res.data['first_name'], 'Desmond')
        self.assertEquals(res.status_code, 201)
    
    def test_user_sign_up_create_no_data(self):
        #set user data
        request_data = {}

        #Get user data from response
        res = self.client.post(self.list_url, request_data)

        #check if data is correct
        self.assertEquals(res.status_code, 400)


class TestUserLogInViewSet(TestCase):
    
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.list_url = reverse('user-log-in-list')
        date_time_str = '12/31/1990'
        self.date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y')

        self.user = User.objects.create(
            first_name = "Desmond",
            last_name = 'Fox',
            email = 'fox@foxbecoding.com',
            password = make_password('123456'),
            date_of_birth = self.date_time_obj.date(),
            agreed_to_toa = True
        )
        self.user.save()

    def test_user_log_in_create(self):
        #set user data
        request_data = {
            'email': 'fox@foxbecoding.com',
            'password': '123456'
        }
    
        #Get user data from response
        res = self.client.post(self.list_url, request_data)

        # csrf_token = self.client.cookies['csrftoken'].value
        # print(csrf_token)

        #check if data is correct
        self.assertGreater(len(res.data['logins']), 0)
        self.assertEquals(res.data['first_name'], 'Desmond')
        self.assertEquals(res.status_code, 202)

    def test_user_log_in_create_failed(self):
        #set user data
        request_data = {
            'email': 'fox@foxbecoding.com',
        }
    
        #Get user data from response
        res = self.client.post(self.list_url, request_data)

        #check if data is correct
        self.assertEquals(res.status_code, 400)

# class TestUserLogOutViewSet(TestCase):
    
#     def setUp(self):
#         self.client = Client()
#         self.list_url = reverse('user-log-out-list')
#         date_time_str = '12/31/1990'
#         self.date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y')

#         self.user = User.objects.create(
#             first_name = "Desmond",
#             last_name = 'Fox',
#             email = 'fox@foxbecoding.com',
#             password = make_password('123456'),
#             date_of_birth = self.date_time_obj.date(),
#             agreed_to_toa = True
#         )
#         self.user.save()

#     def test_user_log_out_create(self):
#         #set user data
#         request_data = {}
    
#         #Get user data from response
#         res = self.client.post(self.list_url, request_data)

#         #check if data is correct
#         self.assertEquals(res.status_code, 200)