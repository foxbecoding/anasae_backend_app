from django.test import TestCase, Client
from django.urls import reverse
from users.models import UserGender
from datetime import datetime

is_CSRF = True

class TestMPAUserViewSet(TestCase):
    
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

    def test_mpa_user_retrieve(self):
        res = self.client.get(reverse('mpa-user-detail', kwargs={'pk': self.user['pk']}))
        self.assertEqual(res.status_code, 200)

    def test_mpa_user_retrieve_pk_mismatch(self):
        res = self.client.get(reverse('mpa-user-detail', kwargs={'pk': 0}))
        self.assertEqual(res.status_code, 401)

    def test_mpa_user_update(self):
        request_data = {
            'first_name': 'Slugga',
            'last_name': 'Fox',
        }
        res = self.client.put(
            reverse('mpa-user-detail', kwargs={'pk': self.user['pk']}), 
            content_type='application/json', 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.assertEqual(res.data['first_name'], 'Slugga')
        self.assertEqual(res.status_code, 202)
    
    def test_mpa_user_update_error(self):
        request_data = {
            'first_name': 'Slugga',
            'last_name': '',
        }
        res = self.client.put(
            reverse('mpa-user-detail', kwargs={'pk': self.user['pk']}), 
            content_type='application/json', 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )               
        self.assertEqual(res.status_code, 400)

    def test_mpa_user_update_pk_mismatch(self):
        request_data = {
            'first_name': 'Slugga',
            'last_name': 'Fox'
        }
        res = self.client.put(
            reverse('mpa-user-detail', kwargs={'pk': 0}), 
            content_type='application/json', 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.assertEqual(res.status_code, 401)

class TestMPAUserProfileViewSet(TestCase):
    
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
        

    def test_mpa_user_profile_create(self):
        request_data = { 'name': 'foxbecoding' }
        res = self.client.post(
            reverse('mpa-user-profile-list'), 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.assertGreater(len(res.data['profiles']), 1)
        self.assertEqual(res.status_code, 201)

    
    def test_mpa_user_profile_update(self):
        profile_pk = self.user['profiles'][0]
        request_data = {'name': 'foxbecoding'}
        res = self.client.put(
            reverse('mpa-user-profile-detail', kwargs={'pk': profile_pk}), 
            content_type='application/json', 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.assertEqual(res.data['profiles'][0]['name'], 'foxbecoding')
        self.assertEqual(res.status_code, 202)

    def test_mpa_user_profile_update_error(self):
        profile_pk = self.user['profiles'][0]
        request_data = {'name': ''}
        res = self.client.put(
            reverse('mpa-user-profile-detail', kwargs={'pk': profile_pk}), 
            content_type='application/json', 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.assertEqual(res.status_code, 400)

    def test_mpa_user_profile_update_no_ownership(self):
        profile_pk = 25
        request_data = {'name': 'foxbecoding'}
        res = self.client.put(
            reverse('mpa-user-profile-detail', kwargs={'pk': profile_pk}), 
            content_type='application/json', 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.assertEqual(res.status_code, 401)

    def test_mpa_user_profile_destroy(self):
        #Make additional profile
        res = self.client.post(
            reverse('mpa-user-profile-list'), 
            data={ 'name': 'SoyReyFox' }, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        profile_pk = res.data['profiles'][1]['pk']
        request_data = {}
        res = self.client.delete(
            reverse('mpa-user-profile-detail', kwargs={'pk': profile_pk}), 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.assertEqual(len(res.data['profiles']), 1)
        self.assertEqual(res.status_code, 202)
    
    def test_mpa_user_profile_destroy_error(self):
        #Make additional profile
        self.client.post(
            reverse('mpa-user-profile-list'), 
            data={ 'name': 'SoyReyFox' }, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        profile_pk = self.user['profiles'][0]
        request_data = {}
        res = self.client.delete(
            reverse('mpa-user-profile-detail', kwargs={'pk': profile_pk}), 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.assertEqual(res.status_code, 401)