from django.shortcuts import render
import web_scraper.bs4.bs4_scraper as scraper
from web_scraper.models import HmTable
from rest_framework import generics
from web_scraper.serializers import HmItemsSerializer
from django.shortcuts import redirect


# Create your views here.

class ListHmItemsView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    def get_queryset(self):
        qs = HmTable.objects.values('title', 'item_link', 'regular_price', 'sale_price')
        amount = self.request.query_params.get('amount')
        if amount:
            return qs[:int(amount)]
        else:
            return qs

    serializer_class = HmItemsSerializer

def redirect_view(request):
    response = redirect('/hm/')
    return response

def index(request):
    amount = scraper.hm_url_updater()
    print(amount)
    #manual = scraper.Hm('https://www2.hm.com/en_us/sale/men/view-all.html')
    #manual.update_items()
    hm_db_table = HmTable.objects.all().order_by('pk')[:amount]
    title_list = []
    item_link_list = []
    image_source_list = []
    regular_price_list = []
    sale_price_list = []
    for i in hm_db_table:
        title_list.append(i.title)
        item_link_list.append(i.item_link)
        image_source_list.append(i.image_source)
        regular_price_list.append(i.regular_price)
        sale_price_list.append(i.sale_price)
    rng = range(amount)

    template_name = "web_scraper/index.html"
    context = {
        'range': rng,
        'title_list': title_list,
        'item_link_list': item_link_list,
        'image_source_list': image_source_list,
        'reg_price_list': regular_price_list,
        'sale_price_list': sale_price_list,
    }

    return render(request, template_name, context)
