from rest_framework import serializers
from merchants.models import *
from utils.helpers import create_uid
from PIL import Image
import stripe, requests, os, calendar, time

env = os.getenv

class MerchantSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Merchant
        fields = [
            'pk',
            'uid',
            'title',
            'user',
            'is_active',
            'payment_methods',
            'subscription',
            'stores'
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

class MerchantSubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = MerchantSubcription
        fields = [ 
            'pk',
            'stripe_sub_id'
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

        try:
            Stripe_Payment_Intent = stripe.PaymentIntent.create(
                amount=Stripe_Price.unit_amount,
                currency="usd",
                customer=request.user.stripe_customer_id,
                automatic_payment_methods={"enabled": True},
            )

            Stripe_Payment_Intent = stripe.PaymentIntent.confirm(
                Stripe_Payment_Intent.id,
                payment_method = request.data['payment_method'],
                return_url = os.getenv('STRIPE_PAYMENT_INTENT_RETURN_URL')
            )

            Stripe_Subscription = stripe.Subscription.create(
                customer=request.user.stripe_customer_id,
                items=[
                    {"price": request.data['price_key']},
                ],
                default_payment_method = request.data['payment_method']
            )

            Merchant_Subcription_Instance = MerchantSubcription.objects.create(
                merchant = Merchant.objects.get(user_id=str(request.user.id)),
                merchant_plan = attrs.get('merchant_plan'),
                stripe_sub_id = Stripe_Subscription.id
            )

            Merchant_Subcription_Instance.save()
            attrs['merchant_subscription'] = Merchant_Subcription_Instance
            attrs['merchant'] = Merchant.objects.get(user_id=str(request.user.id))
            return attrs
        except: 
            msg = 'Please use a different payment method.'
            raise serializers.ValidationError({"payment_method": msg}, code='authorization')
        
class MerchantStoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = MerchantStore
        fields = [
            'pk',
            'uid',
            'name',
            'description',
            'stripe_account_id',
            'logo',
            'banner'
        ]

class EditMerchantStoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = MerchantStore
        fields = [
            'name',
            'description',
        ]

class CreateMerchantStoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = MerchantStore
        fields = [
            'name',
            'description'
        ]
    
    def validate(self, attrs):
        request = self.context['request']

        Stripe_Account = stripe.Account.create(
            type="custom",
            country="US",
            email=request.user.email,
            capabilities={
                "card_payments": {"requested": True},
                "transfers": {"requested": True},
            }
        )

        Merchant_Instance = Merchant.objects.get(user_id=str(request.user.id))
        Merchant_Store_Instance = MerchantStore.objects.create(
            merchant = Merchant_Instance,
            uid = create_uid('ms-'),
            stripe_account_id = Stripe_Account.id,
            name = attrs.get('name'),
            description = attrs.get('description')
        )
        Merchant_Store_Instance.save()

        stripe.Account.modify(
            Stripe_Account.id,
            metadata={
                "user_id": request.user.id,
                "merchant_id": Merchant_Instance.id,
                "store_id": Merchant_Store_Instance.id
            },
        )
        
        attrs['merchant'] = Merchant_Instance
        return attrs
    
class MerchantStoreLogoSerializer(serializers.ModelSerializer):

    class Meta:
        model = MerchantStoreLogo
        fields = [
            'pk',
            'merchant_store',
            'image'
        ]

class CreateMerchantStoreLogoSerializer(serializers.ModelSerializer):

    class Meta:
        model = MerchantStoreLogo
        fields = [
            'merchant_store'
        ]
    
    def validate(self, attrs):
        request_data = self.context['request'].data

        if 'image' not in request_data:
            msg = 'Please upload an image'
            raise serializers.ValidationError({"image": msg}, code='authorization')
        
        if not request_data['image']:
            msg = 'Please upload an image'
            raise serializers.ValidationError({"image": msg}, code='authorization')

        image = request_data['image']
        merchant_store = attrs.get('merchant_store')

        img = Image.open(image)
        valid_formats = ['PNG', 'JPEG']
        if img.format not in valid_formats:
            msg = 'Image must be in PNG or JPEG format'
            raise serializers.ValidationError({"image": msg}, code='authorization')
        
        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)
        image_name = create_uid('msl-')+f'-{time_stamp}.{img.format.lower()}'
        image_path = str(env('CDN_MERCHANT_STORE_LOGO_DIR')+image_name)
    
        upload = requests.post(
            f'{env("CDN_HOST_API")}{env("CDN_UPLOAD_IMAGE")}',
            data = {
                "file_path": env('CDN_MERCHANT_STORE_LOGO_DIR'),
                "image_name": image_name
            },
            files={ "image": image.file.getvalue() }
        )

        if upload.status_code != 200:
            msg = 'Please try again'
            raise serializers.ValidationError({"image": msg}, code='authorization')

        Merchant_Store_Logo_Instance = MerchantStoreLogo.objects.create(
            merchant_store = merchant_store,
            image = image_path
        )

        Merchant_Store_Logo_Instance.save()
        attrs['merchant_store_logo'] = Merchant_Store_Logo_Instance
        return attrs

class MerchantStoreBannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = MerchantStoreBanner
        fields = [
            'pk',
            'merchant_store',
            'image',
        ]

class CreateMerchantStoreBannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = MerchantStoreBanner
        fields = [
            'merchant_store'
        ]
    
    def validate(self, attrs):
        request_data = self.context['request'].data

        if 'image' not in request_data:
            msg = 'Please upload an image'
            raise serializers.ValidationError({"image": msg}, code='authorization')
        
        if not request_data['image']:
            msg = 'Please upload an image'
            raise serializers.ValidationError({"image": msg}, code='authorization')

        image = request_data['image']
        merchant_store = attrs.get('merchant_store')

        img = Image.open(image)
        valid_formats = ['PNG', 'JPEG']
        if img.format not in valid_formats:
            msg = 'Image must be in PNG or JPEG format'
            raise serializers.ValidationError({"image": msg}, code='authorization')
        
        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)
        image_name = create_uid('msb-')+f'-{time_stamp}.{img.format.lower()}'
        image_path = str(env('CDN_MERCHANT_STORE_BANNER_DIR')+image_name)
    
        upload = requests.post(
            f'{env("CDN_HOST_API")}{env("CDN_UPLOAD_IMAGE")}',
            data = {
                "file_path": env('CDN_MERCHANT_STORE_BANNER_DIR'),
                "image_name": image_name
            },
            files={ "image": image.file.getvalue() }
        )

        if upload.status_code != 200:
            msg = 'Please try again'
            raise serializers.ValidationError({"image": msg}, code='authorization')

        Merchant_Store_Banner_Instance = MerchantStoreBanner.objects.create(
            merchant_store = merchant_store,
            image = image_path
        )

        Merchant_Store_Banner_Instance.save()
        attrs['merchant_store_banner'] = Merchant_Store_Banner_Instance
        return attrs
    
class MerchantStoreCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = MerchantStoreCategory
        fields = [
            'pk',
            'merchant_store',
            'title',
            'description'
        ]

class CreateMerchantStoreCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = MerchantStoreCategory
        fields = [
            'merchant_store',
            'title',
            'description'
        ]