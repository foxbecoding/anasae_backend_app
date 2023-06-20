from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from categories.models import Category, Subcategory, SubcategorySection
from categories.serializers import *

class MPACategoryViewSet(viewsets.ViewSet):
    lookup_field = "uid"
    
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [ permission() for permission in permission_classes ]

    def list(self, request):
        self.Category_Instance = Category.objects.all()
        data = self.prepare_category_data()
        return Response(data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, uid=None):
        identifier = str(uid).split('-')[0]
        if identifier == 'cat':
            if Category.objects.filter(uid=uid).exists():
                Category_Instance = Category.objects.get(uid=uid)
                Category_Serializer = CategorySerializer(Category_Instance)
                print(Category_Serializer.data)
        elif identifier == 'scat':
            pass
        else:
            pass
        return Response(None, status=status.HTTP_200_OK)

    
    def prepare_category_data(self):
        Category_Serializer = CategorySerializer(self.Category_Instance, many=True)
        data = []
        
        for cat in Category_Serializer.data:
            subcategories = []
            if len(cat['subcategories']) == 0:
                continue       
            for scat in cat['subcategories']:
                Subcategory_Instance = Subcategory.objects.get(pk=scat)
                Subcategory_Serializer = SubcategorySerializer(Subcategory_Instance)
                subcategories.append(Subcategory_Serializer.data)
            
            for scat in subcategories:
                sections = []
                if len(scat['sections']) == 0:
                    continue
                for scats in scat['sections']:
                    Subcategory_Section_Instance = SubcategorySection.objects.get(pk=scats)
                    Subcategory_Section_Serializer = SubcategorySectionSerializer(Subcategory_Section_Instance)
                    sections.append(Subcategory_Section_Serializer.data)                
                scat['sections'] = sections
            
            cat['subcategories'] = subcategories
            data.append(cat)
        return data