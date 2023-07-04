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

    Merchant_Store_Instances = MerchantStore.objects.filter(
        pk__in=Merchant_Serializer.data['stores']
    )
    Merchant_Store_Serializer = MerchantStoreSerializer(
        Merchant_Store_Instances, 
        many=True
    )

    subscription_data = None
    if Merchant_Serializer.data['subscription']:
        Merchant_Subcription_Instance = MerchantSubcription.objects.get(pk=Merchant_Serializer.data['subscription'])
        Merchant_Subscription_Serializer = MerchantSubscriptionSerializer(Merchant_Subcription_Instance)
        subscription_data = Merchant_Subscription_Serializer.data
    
    for store in Merchant_Store_Serializer.data:
        if store['logo']:
            Merchant_Store_Logo_Instance = MerchantStoreLogo.objects.get(pk=store['logo'])
            Merchant_Store_Logo_Serializer = MerchantStoreLogoSerializer(Merchant_Store_Logo_Instance)
            store['logo'] = Merchant_Store_Logo_Serializer.data
        
        if store['banner']:
            Merchant_Store_Banner_Instance = MerchantStoreBanner.objects.get(pk=store['banner'])
            Merchant_Store_Banner_Serializer = MerchantStoreLogoSerializer(Merchant_Store_Banner_Instance)
            store['banner'] = Merchant_Store_Banner_Serializer.data

        store_categories = []
        if len(store['categories']) > 0:
            for cat in store['categories']:
                Merchant_Store_Category_Instance = MerchantStoreCategory.objects.get(pk=cat)
                Merchant_Store_Category_Serializer = MerchantStoreCategorySerializer(Merchant_Store_Category_Instance)
                Merchant_Store_Category_Banner_Instance = MerchantStoreCategoryBanner.objects.get(pk=Merchant_Store_Category_Serializer.data['banner'])
                Merchant_Store_Category_Serializer.data['banner'] = MerchantStoreCategoryBannerSerializer(Merchant_Store_Category_Banner_Instance)
                store_categories.append(Merchant_Store_Category_Serializer.data)
        store['categories'] = store_categories  
        
    return {
        'pk': Merchant_Serializer.data['pk'], 
        'uid': Merchant_Serializer.data['uid'], 
        'title': Merchant_Serializer.data['title'],
        'payment_methods': Merchant_Payment_Method_Serializer.data,
        'subscription': subscription_data,
        'stores': Merchant_Store_Serializer.data
    }