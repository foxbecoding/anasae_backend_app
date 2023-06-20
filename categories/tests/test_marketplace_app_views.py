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
                'title': "Women's Fashion",
                'description': "Best black women's fashion trends"
            },
            {
                'title': "Men's Fashion",
                'description': "Best black men's fashion trends"
            },
            {
                'title': "Bags & Shoes",
                'description': "Best bags & shoes by black designers"
            },
        ]
        
        Category_Instances = []
        for cat in categories:
            Category_Instance = Category.objects.create(
                title = cat['title'],
                description = cat['description']
            )
            Category_Instance.save()
            Category_Instances.append(Category_Instance)

        self.category_data = Category_Instances[0]
        Category_Instances = [ {'category': CI } for CI in Category_Instances ]
        subcategories = [
            {
                'title': "Bottoms",
                'description': "Shop women's pants, leggings, shorts and more."
            },
            {
                'title': "Bottoms",
                'description': "Shop men's pants, jeans, shorts and more."
            },
            {
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
                title = data['title'],
                description = data['description']
            )
            Subcategory_Instance.save()
            Subcategory_Instances.append(Subcategory_Instance)

        self.subcategory_data = Subcategory_Instances[0]
        Subcategory_Instances = [ {'subcategory': SCI } for SCI in Subcategory_Instances ]
        subcategory_sections = [
            {
                'title': "Leggings",
                'description': "Shop women's leggings."
            },
            {
                'title': "Bottoms",
                'description': "Shop men's jeans."
            },
            {
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
                title = data['title'],
                description = data['description']
            )
            Subcategory_Section_Instance.save()
            Subcategory_Section_Instances.append(Subcategory_Section_Instance)
        
        self.subcategory_section_data = Subcategory_Section_Instances[0]

    def test_mpa_category_list(self):
        res = self.client.get(reverse('mpa-category-list'))
        self.assertEqual(res.status_code, 200)

    def test_mpa_category_retrieve(self):
        category = self.category_data.uid
        subcategory = self.subcategory_data.uid
        subcategory_section = self.subcategory_section_data.uid
        category_res = self.client.get(reverse('mpa-category-detail', kwargs={'uid': category}))
        subcategory_res = self.client.get(reverse('mpa-category-detail', kwargs={'uid': subcategory}))
        subcategory_section_res = self.client.get(reverse('mpa-category-detail', kwargs={'uid': subcategory_section}))
        # print(res.data)