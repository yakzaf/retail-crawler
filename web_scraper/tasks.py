from __future__ import absolute_import, unicode_literals
from celery import shared_task
from web_scraper.bs4 import bs4_scraper as scraper


@shared_task
def daily_hm_db_update():
    url = 'https://www2.hm.com/en_us/sale/men/view-all.html'
    test = scraper.Hm(url)
    test.update_items()
    print('this is working!!!')
