from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from merchants.models import *
from merchants.serializers import *
from merchants.permissions import *
from pprint import pprint

class MCMerchantViewSet(viewsets.ViewSet):
    
    lookup_field = "uid"
    
    def get_permissions(self):
        permission_classes = [ IsAuthenticated, MerchantPermission ]
        return [ permission() for permission in permission_classes ]
    
    @method_decorator(csrf_protect)
    def create(self, request):
        Create_Merchant_Serializer = CreateMerchantSerializer(data=request.data, context={'request': request, 'user': request.user })
        if not Create_Merchant_Serializer.is_valid():
            return Response(Create_Merchant_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        merchant_data = Create_Merchant_Serializer.validated_data['merchant']
        Merchant_Serializer = MerchantSerializer(merchant_data)
        data = Merchant_Serializer.data
        return Response(data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, uid=None):
        self.check_object_permissions(request=request, obj={ 'uid': uid })
        Merchant_Instance = Merchant.objects.get(uid=uid)
        Merchant_Serializer = MerchantSerializer(Merchant_Instance)
        data = Merchant_Serializer.data
        return Response(data, status=status.HTTP_200_OK)

class MCMerchantPaymentMethodViewSet(viewsets.ViewSet):
    
    def get_permissions(self):
        permission_classes = [ IsAuthenticated, MerchantPaymentMethodPermission ]
        return [ permission() for permission in permission_classes ]

    def list(self, request):
        setup_intent_res = stripe.SetupIntent.create(
            customer=request.user.stripe_customer_id,
            payment_method_types=["card"],
        )
        return Response(setup_intent_res.client_secret, status=status.HTTP_200_OK)

    @method_decorator(csrf_protect)
    def create(self, request):
        self.check_object_permissions(request=request, obj={})

        Merchant_Instance = Merchant.objects.get(user_id=str(request.user.id))
        payment_method_res = stripe.PaymentMethod.retrieve(id=request.data['payment_method_id'])

        data = {
            'merchant': Merchant_Instance.id,
            'stripe_pm_id': payment_method_res.id
        }
        
        Create_Merchant_Payment_Method_Serializer = CreateMerchantPaymentMethodSerializer(data=data)
        if not Create_Merchant_Payment_Method_Serializer.is_valid():
            return Response(Create_Merchant_Payment_Method_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        Create_Merchant_Payment_Method_Serializer.save()
        data = get_merchant_data(Merchant_Instance)
        return Response(data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk=None):
        self.check_object_permissions(request=request, obj={'pk': pk})
        Merchant_Payment_Method_Instance = MerchantPaymentMethod.objects.get(pk=str(pk))
        Merchant_Payment_Method_Instance.delete()
        stripe.PaymentMethod.detach(Merchant_Payment_Method_Instance.stripe_pm_id)
        Merchant_Instance = Merchant.objects.get(user_id=str(request.user.id))
        data = get_merchant_data(Merchant_Instance)
        return Response(data, status=status.HTTP_202_ACCEPTED)
    
class MCMerchantSubcriptionViewSet(viewsets.ViewSet):
    
    def get_permissions(self):
        permission_classes = [ IsAuthenticated, MerchantSubscriptionPermission ]
        return [ permission() for permission in permission_classes ]
    
    @method_decorator(csrf_protect)
    def create(self, request):
        self.check_object_permissions(request=request, obj={})
        CreateMerchantSubscriptionSerializer(data=request.data, context={'request': request})
        return Response(None, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        self.check_object_permissions(request=request, obj={'pk': str(pk)})
        print('retrieve')
        return Response(None, status=status.HTTP_200_OK)
    
class MCMerchantPlanViewSet(viewsets.ViewSet):

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def list(self, request, pk=None):
        data = get_merchant_plan_data()
        return Response(data, status=status.HTTP_200_OK)

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

def get_merchant_data(merchant: Merchant):
    Merchant_Serializer = MerchantSerializer(merchant)
    Merchant_Payment_Method_Instances = MerchantPaymentMethod.objects.filter(
        pk__in=Merchant_Serializer.data['payment_methods']
    )
    
    Merchant_Payment_Method_Serializer = MerchantPaymentMethodSerializer(
        Merchant_Payment_Method_Instances, 
        many=True
    )

    return {
        'pk': Merchant_Serializer.data['pk'], 
        'uid': Merchant_Serializer.data['uid'], 
        'title': Merchant_Serializer.data['title'],
        'payment_methods': Merchant_Payment_Method_Serializer.data
    }  