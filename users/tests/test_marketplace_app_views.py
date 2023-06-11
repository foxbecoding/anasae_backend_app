from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from django.middleware.csrf import get_token
from users.models import User, UserLogin, UserGender
from datetime import datetime

is_CSRF = True

class TestMAUserViewSet(TestCase):
    
    def setUp(self):
        self.client = Client(enforce_csrf_checks=is_CSRF)
        date_time_str = '12/31/1990'
        self.date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y')
        self.client.get(reverse('x-fct-list'))
        self.csrftoken = self.client.cookies['csrftoken'].value
        self.user_gender = UserGender.objects.create(gender = 'male')
        self.user_gender.save()

        #User Sign up
        request_data = {
            'first_name': "Desmond",
            'last_name': 'Fox',
            'email': 'fox@foxbecoding.com',
            'password': '123456',
            'confirm_password': '123456',
            'date_of_birth': self.date_time_obj.date(),
            'agreed_to_toa': True,
            'gender': self.user_gender.pk
        }

        #Get response data
        self.client.post(reverse('account-sign-up-list'), request_data, **{'HTTP_X_CSRFTOKEN': self.csrftoken})

        #User Login
        request_data = {
            'email': 'fox@foxbecoding.com',
            'password': '123456'
        }
    
        #Get response data
        res = self.client.post(reverse('account-log-in-list'), request_data, **{'HTTP_X_CSRFTOKEN': self.csrftoken})
        self.user = res.data

    def test_ma_user_retrieve(self):
        res = self.client.get(reverse('ma-user-detail', kwargs={'pk': self.user['pk']}))
        
        self.assertEquals(res.status_code, 200)



