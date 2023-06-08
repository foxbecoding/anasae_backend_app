from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login
import stripe


class UserSignUpViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    def create(self, request):
        # serializer = UserSignUpSerializer(data=request.data, context={ 'request': request })
        # if serializer.is_valid():
        #     user_data = serializer.validated_data['user']
        #     stripe_customer = stripe.Customer.create(
        #         email=user_data.email,
        #         name=user_data.fullname,
        #         metadata={
        #             "pk": user_data.id
        #         }                
        #     )
        #     user_data.stripe_cus_id = stripe_customer.id
        #     user = Create().create(user_data)
        #     login(request, user)
        #     user = PrepareUserData().prepare(user.id)
        #     response = Response(user, status=status.HTTP_202_ACCEPTED)
        # else:
        #     response = Response(serializer.errors, status=status.HTTP_202_ACCEPTED)
        # return response
        return Response(None, status=status.HTTP_201_CREATED)