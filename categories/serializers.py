from rest_framework import serializers
from categories.models import *
from utils.helpers import create_uid
from PIL import Image

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'pk',
            'uid',
            'title',
            'description'
        ]