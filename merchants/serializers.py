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
         
class MerchantPaymentMethodSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MerchantPaymentMethod
        fields = [
            'pk',
            'stripe_pm_id'
        ]

class CreateMerchantPaymentMethodSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MerchantPaymentMethod
        fields = [
            'merchant',
            'stripe_pm_id'
        ]

class MerchantPlanSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = MerchantPlan
        fields = [
            'pk',
            'title',
            'description',
            'product_listings',
            'prices',
            'features'
        ]

class MerchantPlanPriceSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = MerchantPlanPrice
        fields = [
            'pk',
            'title',
            'description',
            'price',
            'stripe_price_key'
        ]

class MerchantPlanFeatureSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = MerchantPlanFeature
        fields = [
            'pk',
            'title'
        ]

class CreateMerchantSubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = MerchantSubcription
        fields = [ 
            'merchant_plan'
        ]
    
    def validate(self, attrs):
        request = self.context['request']
        Stripe_Price = stripe.Price.retrieve(request.data['price_key'])

        Stripe_Payment_Intent = stripe.PaymentIntent.create(
            amount=Stripe_Price.unit_amount,
            currency="usd",
            customer=request.user.stripe_customer_id,
            automatic_payment_methods={"enabled": True},
            payment_method=request.data['payment_method']
        )

        Stripe_Payment_Intent = stripe.PaymentIntent.confirm(
            Stripe_Payment_Intent.id,
            payment_method = request.data['payment_method'],
            return_url = 'http://127.0.0.1:3001'
        )

        # Test & validate on the PaymentIntent confirm statuses

        Stripe_Subscription = stripe.Subscription.create(
            customer=request.user.stripe_customer_id,
            items=[
                {"price": request.data['price_key']},
            ],
            default_payment_method = request.data['payment_method']
        )

        # print(Stripe_Payment_Intent)
        # print(Stripe_Subscription)
        Merchant_Subcription_Instance = MerchantSubcription.objects.create(
            merchant = Merchant.objects.get(user_id=str(request.user.id)),
            merchant_plan = attrs.get('merchant_plan'),
            stripe_sub_id = Stripe_Subscription.id
        )

        Merchant_Subcription_Instance.save()
        attrs['merchant_subscription'] = Merchant_Subcription_Instance
        attrs['merchant'] = Merchant.objects.get(user_id=str(request.user.id))
        return attrs 