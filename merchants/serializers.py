from rest_framework import serializers
from merchants.models import *
from utils.helpers import create_uid
from PIL import Image
import stripe, os

class MerchantSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Merchant
        fields = [
            'pk',
            'uid',
            'title',
            'user',
            'is_active',
            'payment_methods'
        ]

class CreateMerchantSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Merchant
        fields = [
            'title'
        ]
    
    def validate(self, attrs):
        user = self.context['user']
        Merchant_Instance = Merchant.objects.create(
            user = user,
            uid = create_uid('m-'),
            title = attrs.get('title'),
        )

        Merchant_Instance.save()
        attrs['merchant'] = Merchant_Instance
        return attrs 
    
class CreateMerchantPaymentMethodSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MerchantPaymentMethod
        fields = [
            'merchant',
            'stripe_pm_id'
        ]