from rest_framework import serializers
from categories.models import *
from utils.helpers import create_uid
from PIL import Image

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'pk',
            'uid',
            'title',
            'description',
            'subcategories'
        ]

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = [
            'pk',
            'uid',
            'title',
            'description',
            'sections'
        ]