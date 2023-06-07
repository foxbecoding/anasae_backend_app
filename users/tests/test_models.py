from django.test import TestCase
from users.models import *
from datetime import datetime

class TestModels(TestCase):

    def setUp(self):
        # date_time_str = '12/31/1990'
        # date_time_obj = datetime.strptime(date_time_str, '%m/%d/%y')
        # print(date_time_obj)
        self.user = User.objects.create(
            first_name = "Desmond",
            last_name = 'Fox',
            username = 'foxbecoding',
            email = 'fox@foxbecoding.com',
            agreed_to_toa = True,
            stripe_customer_id = 'ushd89u3hbeuid' 
        )
        self.user.save()

    def test_user_assigned_uid_on_creation(self):
        self.assertGreater(len(self.user.uid), 0)