from django.test import TestCase, Client
from django.urls import reverse
from users.models import User, UserGender, UserProfile, UserAddress
from datetime import datetime
from PIL import Image
import tempfile

is_CSRF = True

def tmp_image(img_format = 'jpg'):
    image = Image.new('RGB', (100, 100))
    tmp_file = tempfile.NamedTemporaryFile(suffix='.{}'.format(img_format), prefix="test_img_")
    if img_format == 'jpg':
        img_format = 'jpeg'
    image.save(tmp_file, img_format)
    tmp_file.seek(0)
    return tmp_file


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

    def test_mpa_user_retrieve_permissions_failed(self):
        res = self.client.get(reverse('mpa-user-detail', kwargs={'pk': 0}))
        self.assertEqual(res.status_code, 403)

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

    def test_mpa_user_update_permissions_failed(self):
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
        self.assertEqual(res.status_code, 403)

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

        account_res = self.client.post(
            reverse('account-sign-up-list'), 
            user_sign_up_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        user = User.objects.get(pk=account_res.data['pk'])

        user_profile = UserProfile.objects.create(
            user = user,
            name = 'KingFox'
        )
        user_profile.save()

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
        self.assertEqual(res.data['profiles'][2]['name'], 'foxbecoding')
        self.assertEqual(res.status_code, 201)
    
    def test_mpa_user_profile_create_error(self):
        request_data = {}
        res = self.client.post(
            reverse('mpa-user-profile-list'), 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.assertEqual(res.status_code, 400)
    
    def test_mpa_user_profile_update(self):
        profile_pk = self.user['profiles'][0]
        request_data = {'name': 'foxbecoding'}
        res = self.client.put(
            reverse('mpa-user-profile-detail', kwargs={'pk': profile_pk}), 
            content_type='application/json', 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.assertEqual(res.data['profiles'][1]['name'], 'foxbecoding')
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
        profile_pk = 1000
        request_data = {'name': 'foxbecoding'}
        res = self.client.put(
            reverse('mpa-user-profile-detail', kwargs={'pk': profile_pk}), 
            content_type='application/json', 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.assertEqual(res.status_code, 401)

    def test_mpa_user_profile_destroy(self):
        profile_pk = self.user['profiles'][1]
        request_data = {}
        res = self.client.delete(
            reverse('mpa-user-profile-detail', kwargs={'pk': profile_pk}), 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.assertEqual(len(res.data['profiles']), 1)
        self.assertEqual(res.status_code, 202)
    
    def test_mpa_user_profile_destroy_error(self):
        profile_pk = self.user['profiles'][0]
        request_data = {}
        res = self.client.delete(
            reverse('mpa-user-profile-detail', kwargs={'pk': profile_pk}), 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.assertEqual(res.status_code, 401)

class TestMPAUserProfileImageViewSet(TestCase):
    
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
        

    def test_mpa_user_profile_image_create(self):
        request_data = {
            'user_profile': self.user['profiles'][0],
            'image': tmp_image()
        }
        res = self.client.post(
            reverse('mpa-user-profile-image-list'), 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
  
        self.assertNotEqual(res.data['profiles'][0]['image'], None)
        self.assertEqual(res.status_code, 201)   

    def test_mpa_user_profile_image_create_error(self):
        request_data = {
            'user_profile': self.user['profiles'][0],
            'image': tmp_image('gif')
        }
        res = self.client.post(
            reverse('mpa-user-profile-image-list'), 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.assertEqual(res.status_code, 400)
    
    def test_mpa_user_profile_image_create_no_ownership(self):
        request_data = {
            'user_profile': 1111,
            'image': tmp_image('png')
        }
        res = self.client.post(
            reverse('mpa-user-profile-image-list'), 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.assertEqual(res.status_code, 401)

    def test_mpa_user_profile_image_update(self):
        create_image_request_data = {
            'user_profile': self.user['profiles'][0],
            'image': tmp_image('png')
        }
        create_image_res = self.client.post(
            reverse('mpa-user-profile-image-list'), 
            data=create_image_request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        update_image_request_data = {
            'user_profile': self.user['profiles'][0],
            'image': tmp_image('png')
        }
        update_image_res = self.client.post(
            reverse('mpa-user-profile-image-list'),
            data=update_image_request_data,
            **{ 'HTTP_X_CSRFTOKEN': self.csrftoken }
        )
        self.assertEqual(create_image_res.status_code, 201)
        self.assertEqual(update_image_res.status_code, 201)

class TestMPAUserAddressViewSet(TestCase):
    
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

        account_res = self.client.post(
            reverse('account-sign-up-list'), 
            user_sign_up_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )


        user = User.objects.get(pk=account_res.data['pk'])
        user_profile = UserProfile.objects.create(
            user = user,
            name = 'KingFox'
        )
        user_profile.save()

        self.user_address = UserAddress.objects.create(
            user = user,
            full_name = 'Desmond Fox',
            phone_number = '(504)366-7899',
            street_address = '1912 Pailet',
            street_address_ext = '',
            country = 'United States',
            state = 'Louisiana',
            city = 'Harvey',
            postal_code = '70058'
        )

        self.user_address.save()

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
        

    def test_mpa_user_address_create(self):
        request_data = { 
            'full_name': 'Desmond Fox',
            'phone_number': '(504)729-8617',
            'street_address': '4024 Crossmoor dr',
            'street_address_ext': '',
            'country': 'United States',
            'state': 'Louisiana',
            'city': 'Marrero',
            'postal_code': '70072'
        }
        res = self.client.post(
            reverse('mpa-user-address-list'), 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.assertEqual(res.data['addresses'][1]['city'], 'Marrero')
        self.assertEqual(res.status_code, 201)
    
    def test_mpa_user_address_create_error(self):
        request_data = { 
            'full_name': '',
            'phone_number': '(504)729-8617',
            'street_address': '4024 Crossmor dr',
            'street_address_ext': '',
            'country': 'United States',
            'state': 'Louisiana',
            'city': 'Marrero',
            'postal_code': '70072'
        }
        res = self.client.post(
            reverse('mpa-user-address-list'), 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.assertEqual(res.status_code, 400)

    def test_mpa_user_address_update(self):
        request_data = { 
            'full_name': 'Desmond L Fox',
            'phone_number': '(504)729-8617',
            'street_address': '4024 Crossmor dr',
            'street_address_ext': '',
            'country': 'United States',
            'state': 'Louisiana',
            'city': 'Marrero',
            'postal_code': '70072',
            'is_default': True
        }
        res = self.client.put(
            reverse('mpa-user-address-detail', kwargs={'pk': self.user_address.id}),
            content_type='application/json',
            data=request_data,  
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ) 
        self.assertEqual(res.status_code, 202)

    def test_mpa_user_address_update_error(self):
        request_data = { 
            'full_name': '',
            'phone_number': '(504)729-8617',
            'street_address': '4024 Crossmor dr',
            'street_address_ext': '',
            'country': 'United States',
            'state': 'Louisiana',
            'city': 'Marrero',
            'postal_code': '70072',
            'is_default': True
        }
        res = self.client.put(
            reverse('mpa-user-address-detail', kwargs={'pk': self.user_address.id}),
            content_type='application/json',
            data=request_data,  
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ) 
        self.assertEqual(res.status_code, 400)

    def test_mpa_user_address_update_no_ownership(self):
        request_data = { 
            'full_name': 'Desmond L Fox',
            'phone_number': '(504)729-8617',
            'street_address': '4024 Crossmor dr',
            'street_address_ext': '',
            'country': 'United States',
            'state': 'Louisiana',
            'city': 'Marrero',
            'postal_code': '70072',
            'is_default': True
        }
        res = self.client.put(
            reverse('mpa-user-address-detail', kwargs={'pk': 847}),
            content_type='application/json',
            data=request_data,  
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ) 
        self.assertEqual(res.status_code, 401)
    
    def test_mpa_user_address_destroy(self):
        request_data = {}
        res = self.client.delete(
            reverse('mpa-user-address-detail', kwargs={'pk': self.user_address.id}),
            content_type='application/json',
            data=request_data,  
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ) 
        self.assertEqual(res.status_code, 202)
    
    def test_mpa_user_address_destroy_no_ownership(self):
        request_data = {}
        res = self.client.delete(
            reverse('mpa-user-address-detail', kwargs={'pk': 847}),
            content_type='application/json',
            data=request_data,  
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ) 
        self.assertEqual(res.status_code, 401)