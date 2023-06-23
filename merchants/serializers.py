from rest_framework import serializers
from merchants.models import *
from utils.helpers import create_uid
from PIL import Image
import stripe

class MerchantSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Merchant
        fields = [
            'pk',
            'uid',
            'title',
            'user',
            'is_active'
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
    
    # Create fields for card info
    card_number = serializers.CharField(write_only=True)
    card_exp_month = serializers.IntegerField(write_only=True)
    card_exp_year = serializers.IntegerField(write_only=True)
    card_cvc = serializers.CharField(write_only=True)
    
    class Meta:
        model = MerchantPaymentMethod
        fields = [
            'card_number',
            'card_exp_month',
            'card_exp_year',
            'card_cvc'
        ]

    def validate(self, attrs):
        user_id = str(self.context['request'].user.id)
        Merchant_Instance = Merchant.objects.get(user_id=user_id)
        
        res = stripe.PaymentMethod.create(
            type="card",
            card={
                "number": str(attrs.get('card_number')),
                "exp_month": int(attrs.get('card_exp_month')),
                "exp_year": int(attrs.get('card_exp_year')),
                "cvc": str(attrs.get('card_cvc')),
            }
        )
        print(res)
        
        # attrs['merchant'] = Merchant_Instance
        return attrs 