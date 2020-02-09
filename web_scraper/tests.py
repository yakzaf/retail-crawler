from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from web_scraper.models import HmTable
from web_scraper.serializers import HmItemsSerializer
from django.utils import timezone

# Create your tests here.

# tests for views


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def new_sale_items(title='', item_link='', regular_price='', sale_price=''):
        if title != '' and regular_price != '' and sale_price != '':
            HmTable.objects.create(title=title, item_link=item_link,
                                   regular_price=regular_price, sale_price=sale_price, update_time=timezone.now())

    def setUp(self):
        # add test data
        self.new_sale_items('Test1', 'https://www2.hm.com/en_us/productpage.0685813006.html',
                            regular_price='50', sale_price='10')
        self.new_sale_items('Test2', 'https://www2.hm.com/en_us/productpage.0798938003.html',
                            regular_price='60', sale_price='20')
        self.new_sale_items('Test3', 'https://www2.hm.com/en_us/productpage.0599945008.html',
                            regular_price='70', sale_price='30')
        self.new_sale_items('Test4', 'https://www2.hm.com/en_us/productpage.0843981001.html',
                            regular_price='80', sale_price='40')
        self.new_sale_items('Test5', 'https://www2.hm.com/en_us/productpage.0533404021.html',
                            regular_price='90', sale_price='50')


class GetAllItemsTest(BaseViewTest):

    def test_get_all_items(self):
        """
        This test ensures that all items added in the set_up method
        exist when we make a GET request to the hm/ endpoint
        """
        # hit the api endpoint
        response = self.client.get(reverse("web_scraper:items-all"))
        # fetch the data from db
        expected = HmTable.objects.all()
        serialized = HmItemsSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_certain_amount(self):
        """
        This test checks the parameters
        """
        # hit the api endpoint with parameters
        response = self.client.get(reverse("web_scraper:items-all"), {'amount': '3'})
        # fetch the correct amount from db
        expected = HmTable.objects.all()[:3]
        serialized = HmItemsSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)