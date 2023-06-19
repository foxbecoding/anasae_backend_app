from django.test import TestCase, Client
from django.urls import reverse
from categories.models import *
from utils.helpers import create_uid
from pprint import pprint

class TestMPAUserViewSet(TestCase):
    
    def setUp(self):
        self.client = Client()
        categories = [
            {
                'uid': create_uid('cat-'),
                'title': "Women's Fashion",
                'description': "Best black women's fashion trends"
            },
            {
                'uid': create_uid('cat-'),
                'title': "Men's Fashion",
                'description': "Best black men's fashion trends"
            },
            {
                'uid': create_uid('cat-'),
                'title': "Bags & Shoes",
                'description': "Best bags & shoes by black designers"
            },
        ]
        
        Category_Instances = []
        for cat in categories:
            Category_Instance = Category.objects.create(
                uid = cat['uid'],
                title = cat['title'],
                description = cat['description']
            )
            Category_Instance.save()
            Category_Instances.append(Category_Instance)

        Category_Instances = [ {'category': CI } for CI in Category_Instances ]
        subcategories = [
            {
                'uid': create_uid('scat-'),
                'title': "Bottoms",
                'description': "Shop women's pants, leggings, shorts and more."
            },
            {
                'uid': create_uid('scat-'),
                'title': "Bottoms",
                'description': "Shop men's pants, jeans, shorts and more."
            },
            {
                'uid': create_uid('scat-'),
                'title': "Women's Shoes",
                'description': "Shop top black brands for women shoes"
            }, 
        ]

        subcategories = zip(subcategories, Category_Instances)
        Subcategory_Instances = []
        for scat in subcategories:
            data = scat[0]
            category = scat[1]['category']
            Subcategory_Instance = Subcategory.objects.create(
                category = category,
                uid = data['uid'],
                title = data['title'],
                description = data['description']
            )
            Subcategory_Instance.save()
            Subcategory_Instances.append(Subcategory_Instance)

        Subcategory_Instances = [ {'subcategory': SCI } for SCI in Subcategory_Instances ]
        subcategory_sections = [
            {
                'uid': create_uid('scats-'),
                'title': "Leggings",
                'description': "Shop women's leggings."
            },
            {
                'uid': create_uid('scats-'),
                'title': "Bottoms",
                'description': "Shop men's jeans."
            },
            {
                'uid': create_uid('scats-'),
                'title': "Women's Shoes",
                'description': "Shop women's flats"
            }, 
        ]

        subcategory_sections = zip(subcategory_sections, Subcategory_Instances)
        Subcategory_Section_Instances = []
        for scats in subcategory_sections:
            data = scats[0]
            subcategory = scats[1]['subcategory']
            Subcategory_Section_Instance = SubcategorySection.objects.create(
                subcategory = subcategory,
                uid = data['uid'],
                title = data['title'],
                description = data['description']
            )
            Subcategory_Section_Instance.save()
            Subcategory_Section_Instances.append(Subcategory_Section_Instance)

    def test_mpa_category_list(self):
        res = self.client.get(reverse('mpa-category-list'))
        self.assertEqual(res.status_code, 200)