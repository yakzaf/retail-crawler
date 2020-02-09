from bs4 import BeautifulSoup

import requests

from web_scraper.models import HmTable

from django.utils import timezone

from django.conf import settings


def hm_url_updater():
    url = 'https://www2.hm.com/en_us/sale/men/view-all.html'
    agent = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

    r = requests.get(url, headers=agent)

    soup = BeautifulSoup(r.content, 'lxml')

    h2_load_more = soup.find("div", {"class": "load-more-products"}).find("h2", {"class": "load-more-heading"})
    data_total = h2_load_more.attrs["data-total"]
    data_total = int(data_total)
    return data_total


class Hm:
    def __init__(self, url):
        data_total = hm_url_updater()
        self.url = url + f"?page-size={data_total}"
        agent = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) '
                               'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
        self.r = requests.get(self.url, headers=agent)
        self.soup = BeautifulSoup(self.r.content, 'lxml')

    def get_hm_list(self):
        hm_list = self.soup.find("ul", {"class": "products-listing"})

        return hm_list

    def get_hm_items(self):
        hm_list = self.get_hm_list()

        hm_items = hm_list.findChildren("li", {"class": "product-item"})

        return hm_items

    def get_hm_items_links(self):
        hm_items_links = ['https://www2.hm.com' + i.attrs["href"] for i in self.get_image_info()]

        return hm_items_links

    def get_image_info(self):
        hm_items = self.get_hm_items()

        image_info = [i.find("div", {"class": "image-container"}).find("a") for i in hm_items]

        return image_info

    def get_titles(self):
        titles = [i.attrs["title"] for i in self.get_image_info()]

        return titles

    def get_image_sources(self):
        image_sources = ['https:' + i.img["data-src"] for i in self.get_image_info()]

        return image_sources

    def get_reg_prices(self):
        reg_prices = [i.find("div", {"class": "item-details"}).strong.find("span", {"class": "price regular"}).text[2:]
                      for i in self.get_hm_items()]
        reg_prices = [float(i) for i in reg_prices]
        return reg_prices

    def get_sale_prices(self):
        sale_prices = [i.find("div", {"class": "item-details"}).strong.find("span", {"class": "price sale"}).text[2:]
                       for i in self.get_hm_items()]
        sale_prices = [float(i) for i in sale_prices]
        return sale_prices

    # def create_items(self):
    #     self.show_all_items()
    #     titles = self.get_titles()
    #     items_links = self.get_hm_items_links()
    #     image_sources = self.get_image_sources()
    #     regular_prices = self.get_reg_prices()
    #     sale_prices = self.get_sale_prices()
    #
    #     for i in range(len(titles)):
    #         item = HmTable(title=titles[i], item_link=items_links[i], image_source=image_sources[i],
    #                        regular_price=regular_prices[i], sale_price=sale_prices[i])
    #         item.save()

    def save_images(self):
        path_names = []
        image_urls = self.get_image_sources()

        for index, image_url in enumerate(image_urls):
            request = requests.get(image_url, stream=True)
            if request.status_code != requests.codes.ok:
                continue
            path = settings.MEDIA_URL+f'{str(index)}.png'
            print(path)
            with open(path, 'wb') as f:
                for block in request.iter_content(1024 * 1024 * 10):
                    if not block:
                        break
                    f.write(block)
                path_names.append(f.name)
        return path_names

    def update_items(self):
        titles = self.get_titles()
        item_links = self.get_hm_items_links()
        image_sources = self.save_images()
        # image_sources = [f'/media/{x}.png' for x in range(len(titles))]
        regular_prices = self.get_reg_prices()
        sale_prices = self.get_sale_prices()
        hm_list = HmTable.objects.all().order_by('pk')
        for c, i in enumerate(hm_list):
            if c >= len(item_links):
                print('break')
                break
            print(c)
            i.title = titles[c]
            i.item_link = item_links[c]
            i.image_source = image_sources[c]
            i.regular_price = regular_prices[c]
            i.sale_price = sale_prices[c]
            i.update_time = timezone.now()
            i.save()
        if len(hm_list) < len(item_links):
            c = 0
            while c < len(item_links):
                item = HmTable(title=titles[c], item_link=item_links[c], image_source=image_sources[c],
                               regular_price=regular_prices[c], sale_price=sale_prices[c],
                               update_time=timezone.now())
                item.save()
                c += 1
