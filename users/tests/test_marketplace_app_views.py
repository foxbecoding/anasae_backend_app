from django.test import TestCase, Client
from django.urls import reverse
from users.models import UserGender
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

        self.client.post(reverse('account-sign-up-list'), user_sign_up_data, **{'HTTP_X_CSRFTOKEN': self.csrftoken})

        #User Login
        request_data = {
            'email': 'fox@foxbecoding.com',
            'password': '123456'
        }
    
        #Get response data
        res = self.client.post(reverse('account-log-in-list'), request_data, **{'HTTP_X_CSRFTOKEN': self.csrftoken})
        self.user = res.data

        self.csrftoken = self.client.cookies['csrftoken'].value

    def test_ma_user_retrieve(self):
        res = self.client.get(reverse('ma-user-detail', kwargs={'pk': self.user['pk']}))
        self.assertEqual(res.status_code, 200)

    def test_ma_user_retrieve_pk_mismatch(self):
        res = self.client.get(reverse('ma-user-detail', kwargs={'pk': 0}))
        self.assertEqual(res.status_code, 400)

    def test_ma_user_update(self):
        request_data = {
            'first_name': 'Slugga',
            'last_name': 'Fox',
        }

        res = self.client.put(reverse('ma-user-detail', kwargs={'pk': self.user['pk']}), content_type='application/json', data=request_data, **{'HTTP_X_CSRFTOKEN': self.csrftoken})
        
        self.assertEqual(res.data['first_name'], 'Slugga')
        self.assertEqual(res.status_code, 202)
    
    def test_ma_user_update_error(self):
        request_data = {
            'first_name': 'Slugga',
            'last_name': '',
        }

        res = self.client.put(reverse('ma-user-detail', kwargs={'pk': self.user['pk']}), content_type='application/json', data=request_data, **{'HTTP_X_CSRFTOKEN': self.csrftoken})               
        self.assertEqual(res.status_code, 400)

    def test_ma_user_update_pk_mismatch(self):
        request_data = {
            'first_name': 'Slugga',
            'last_name': 'Fox'
        }

        res = self.client.put(reverse('ma-user-detail', kwargs={'pk': 0}), content_type='application/json', data=request_data, **{'HTTP_X_CSRFTOKEN': self.csrftoken})
        self.assertEqual(res.status_code, 400)

class TestMAUserProfileViewSet(TestCase):
    
    def setUp(self):
        self.client = Client(enforce_csrf_checks=is_CSRF)
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

        self.client.post(reverse('account-sign-up-list'), user_sign_up_data, **{'HTTP_X_CSRFTOKEN': self.csrftoken})

        #User Login
        request_data = {
            'email': 'fox@foxbecoding.com',
            'password': '123456'
        }
    
        #Get response data
        res = self.client.post(reverse('account-log-in-list'), request_data, **{'HTTP_X_CSRFTOKEN': self.csrftoken})
        self.user = res.data

        self.csrftoken = self.client.cookies['csrftoken'].value

    def test_ma_user_profile_create(self):
        request_data = {
            'name': 'foxbecoding'
        }

        res = self.client.post(reverse('ma-user-profile-list'), data=request_data, **{'HTTP_X_CSRFTOKEN': self.csrftoken})
        
        # self.assertEqual(res.data['first_name'], 'Slugga')
        self.assertEqual(res.status_code, 201)