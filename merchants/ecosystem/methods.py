from merchants.models import *
from merchants.serializers import *

def get_merchant_plan_data():
    Merchant_Plan_Instances = MerchantPlan.objects.all()
    Merchant_Plan_Serializer = MerchantPlanSerializer(Merchant_Plan_Instances, many=True)
    Merchant_Plan_Price_Instances = MerchantPlanPrice.objects.all()
    Merchant_Plan_Price_Serializer = MerchantPlanPriceSerializer(Merchant_Plan_Price_Instances, many=True)
    Merchant_Plan_Feature_Instances = MerchantPlanFeature.objects.all()
    Merchant_Plan_Feature_Serializer = MerchantPlanFeatureSerializer(Merchant_Plan_Feature_Instances, many=True)
    
    data = []
    
    for plan_data in Merchant_Plan_Serializer.data:
        data.append(
            {
                'pk': plan_data['pk'],
                'title': plan_data['title'],
                'description': plan_data['description'],
                'product_listings': plan_data['product_listings'],
                'prices': [ price for price in Merchant_Plan_Price_Serializer.data if price['pk'] in plan_data['prices'] ],
                'features': [ feature for feature in Merchant_Plan_Feature_Serializer.data if feature['pk'] in plan_data['features'] ]
            }
        )
        
    return data

def get_merchant_data(instance: Merchant):
    Merchant_Serializer = MerchantSerializer(instance)
    
    Merchant_Payment_Method_Instances = MerchantPaymentMethod.objects.filter(
        pk__in=Merchant_Serializer.data['payment_methods']
    )
    Merchant_Payment_Method_Serializer = MerchantPaymentMethodSerializer(
        Merchant_Payment_Method_Instances, 
        many=True
    )

    subscription_data = None
    if Merchant_Serializer.data['subscription']:
        Merchant_Subcription_Instance = MerchantSubcription.objects.get(pk=Merchant_Serializer.data['subscription'])
        Merchant_Subscription_Serializer = MerchantSubscriptionSerializer(Merchant_Subcription_Instance)
        subscription_data = Merchant_Subscription_Serializer.data
    
    return {
        'pk': Merchant_Serializer.data['pk'], 
        'uid': Merchant_Serializer.data['uid'], 
        'title': Merchant_Serializer.data['title'],
        'payment_methods': Merchant_Payment_Method_Serializer.data,
        'subscription': subscription_data
    }