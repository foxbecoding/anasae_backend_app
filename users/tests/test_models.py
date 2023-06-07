from django.test import TestCase
from users.models import *

class TestModels(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            
        )