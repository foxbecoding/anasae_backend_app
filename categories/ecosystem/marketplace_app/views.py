from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from categories.models import Category, Subcategory
from categories.serializers import CategorySerializer, SubcategorySerializer

class MPACategoryViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def list(self, request):
        self.Category_Instance = Category.objects.all()
        data = self.prepare_category_data()
        return Response(data, status=status.HTTP_200_OK)
    
    def prepare_category_data(self):
        Category_Serializer = CategorySerializer(self.Category_Instance, many=True)
        data = []
        
        for cat in Category_Serializer.data:
            subcategories = []
            if len(cat['subcategories']) == 0:
                continue
            for scat in cat['subcategories']:
                sections = []
                Subcategory_Instance = Subcategory.objects.get(pk=scat)
                Subcategory_Serializer = SubcategorySerializer(Subcategory_Instance)
                subcategories.append(Subcategory_Serializer.data)
            cat['subcategories'] = subcategories
            data.append(cat)

        return data