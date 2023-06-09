from django.test import TestCase
from users.models import *
from datetime import datetime

class TestModels(TestCase):

    def setUp(self):
        date_time_str = '12/31/1990'
        date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y')
    
        self.user = User.objects.create(
            first_name = "Desmond",
            last_name = 'Fox',
            email = 'fox@foxbecoding.com',
            date_of_birth = date_time_obj.date(),
            agreed_to_toa = True
        )
        # self.user.save()

    def test_user_assigned_uid_on_creation(self):
        self.assertGreater(len(self.user.uid), 0)