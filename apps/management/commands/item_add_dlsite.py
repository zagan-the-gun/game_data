from django.core.management import BaseCommand
from ...models import Item

import json
import requests
import re

import math

from bs4 import BeautifulSoup

import xml.etree.ElementTree as ET

import datetime
import pytz


class Command(BaseCommand):
    help = 'アイテム情報収集'

#    def add_arguments(self, parser):
#        parser.add_argument('-c', '--command', dest='command', help='add or del')
#        parser.add_argument('opt1', help='必須オプション')
#        parser.add_argument('--opt2', help='任意オプション')
#        parser.add_argument('--date', help='何日前')
 
    def handle(self, *args, **options):
#        print(options['command'])
        self.stdout.write(self.style.SUCCESS('DEBUG DEBUG DEBUG item_add: '))
#        self.stdout.write(options.__str__())


        print('dlsiteからJSONでエロゲ商品情報取得')
        dlsite_url = 'https://www.dlsite.com/pro/fsr/=/language/jp/ana_flg/off/work_category%5B0%5D/pc/order%5B0%5D/trend/genre_and_or/or/options_and_or/or/per_page/30/show_type/1/from/fsr.again/keyword/%E5%89%B2%E5%BC%95'
        soup = BeautifulSoup(requests.get(dlsite_url).text, 'lxml')

        for tr in soup.find_all('tr', class_="",):

            if tr.find('span', class_='work_price discount'):

                dlsite_title = tr.a.find('img', ref='popup_img').get('alt')
                print('dlsite_title: ' + dlsite_title)

#                dlsite_image_url = 'https:' + tr.a.find('img', ref='popup_img').get('src')
#                print('dlsite_image_url: ' + dlsite_image_url)

                dlsite_site_url = tr.a.get('href')
                print('dlsite_site_url: ' + dlsite_site_url)

                dlsite_image_url = 'https:' + BeautifulSoup(requests.get(dlsite_site_url).text, 'lxml').find('img', itemprop='image').get('src')
                print('dlsite_image_url: ' + dlsite_image_url)

                dlsite_description_text = tr.find('dd', class_='work_text').get_text()
                print('dlsite_description_text: ' + dlsite_description_text)

                _p = re.search(r'([0-9.,]+)円', tr.find('span', class_='work_price discount').get_text())
                dlsite_price = int(_p.group(1).replace(',', ''))
                print('dlsite_price: ' + str(dlsite_price))

                _pd = re.search(r'(.*日)', tr.find('span', class_='period_date').get_text())
                #dlsite_period_at = datetime.datetime.strptime(_pd.group(1), '%Y年%m月%d日').replace(tzinfo=pytz.timezone('Asia/Tokyo'))
                #dlsite_period_at = datetime.datetime.strptime(_pd.group(1) + ' 23:59:59', '%Y年%m月%d日 %H:%M:%S')
                dlsite_period_at = pytz.timezone('Asia/Tokyo').localize(datetime.datetime.strptime(_pd.group(1) + ' 23:59:59', '%Y年%m月%d日 %H:%M:%S'))
                print('dlsite_period_at: ' + str(dlsite_period_at))

                _d = re.search(r'([0-9]+)%', tr.find('span', class_='icon_campaign type_sale').get_text())
                dlsite_discount_rate = int(_d.group(1))
                print('dlsite_discount_rate: ' + str(dlsite_discount_rate))

                spec_list = BeautifulSoup(requests.get(dlsite_site_url).text, 'lxml').find('dl', class_='work_spec_list')
                _mb = re.search(r'([0-9]+\.[0-9]+)MB\n', spec_list.get_text())
                if _mb is None:
                    dlsite_size = 0

                    # GB表記の処理
                    _gb = re.search(r'([0-9]+\.[0-9]+)GB', spec_list.get_text())
                    if _gb is not None:
                        dlsite_size = float(_gb.group(1))*1024

                else:
                    dlsite_size = float(_mb.group(1))
                print('dlsite_size: ' + str(dlsite_size))

                dlsite_amino_price = dlsite_price
                if dlsite_size != 0:
                    dlsite_amino_price = math.ceil(dlsite_price/dlsite_size)
                print('dlsite_amino_price: ' + str(dlsite_amino_price))


                item=Item.objects.update_or_create(site_url=dlsite_site_url, defaults={'title': dlsite_title, 'image_url': dlsite_image_url, 'site_url': dlsite_site_url, 'description_text': dlsite_description_text, 'amino_price': dlsite_amino_price, 'price': dlsite_price, 'distributor': 'dlsite', 'size': dlsite_size, 'discount_rate': dlsite_discount_rate, 'period_at': dlsite_period_at, 'item_type': Item.ItemType.XXX_GAME})


        print('dlsiteからJSONでエロ本商品情報取得')
        dlsite_url = 'https://www.dlsite.com/maniax/fsr/=/language/jp/sex_category%5B0%5D/male/ana_flg/off/age_category%5B0%5D/adult/work_category%5B0%5D/doujin/order%5B0%5D/trend/work_type%5B0%5D/MNG/work_type%5B1%5D/SCM/work_type%5B2%5D/ICG/work_type_name%5B0%5D/%E3%83%9E%E3%83%B3%E3%82%AC/work_type_name%5B1%5D/%E5%8A%87%E7%94%BB/work_type_name%5B2%5D/CG%E3%83%BB%E3%82%A4%E3%83%A9%E3%82%B9%E3%83%88/work_type_category%5B0%5D/comic/work_type_category_name%5B0%5D/%E3%83%9E%E3%83%B3%E3%82%AC/genre_and_or/or/options_and_or/or/per_page/30/campaign/campaign/show_type/1'
        soup = BeautifulSoup(requests.get(dlsite_url).text, 'lxml')

        for tr in soup.find_all('tr', class_="",):

            if tr.find('span', class_='work_price discount'):

                dlsite_title = tr.a.find('img', ref='popup_img').get('alt')
                print('dlsite_title: ' + dlsite_title)

#                dlsite_image_url = 'https:' + tr.a.find('img', ref='popup_img').get('src')
#                print('dlsite_image_url: ' + dlsite_image_url)

                dlsite_site_url = tr.a.get('href')
                print('dlsite_site_url: ' + dlsite_site_url)

                dlsite_image_url = 'https:' + BeautifulSoup(requests.get(dlsite_site_url).text, 'lxml').find('img', itemprop='image').get('src')
                print('dlsite_image_url: ' + dlsite_image_url)

                dlsite_description_text = tr.find('dd', class_='work_text').get_text()
                print('dlsite_description_text: ' + dlsite_description_text)

                _p = re.search(r'([0-9.,]+)円', tr.find('span', class_='work_price discount').get_text())
                dlsite_price = int(_p.group(1).replace(',', ''))
                print('dlsite_price: ' + str(dlsite_price))

                _pd = re.search(r'(.*日)', tr.find('span', class_='period_date').get_text())
#                dlsite_period_at = datetime.datetime.strptime(_pd.group(1), '%Y年%m月%d日').replace(tzinfo=pytz.timezone('Asia/Tokyo'))
                dlsite_period_at = pytz.timezone('Asia/Tokyo').localize(datetime.datetime.strptime(_pd.group(1) + ' 23:59:59', '%Y年%m月%d日 %H:%M:%S'))
                print('dlsite_period_at: ' + str(dlsite_period_at))

                _d = re.search(r'([0-9]+)%', tr.find('span', class_='icon_campaign type_sale').get_text())
                dlsite_discount_rate = int(_d.group(1))
                print('dlsite_discount_rate: ' + str(dlsite_discount_rate))

                #spec_list = BeautifulSoup(requests.get(dlsite_site_url).text, 'lxml').find('dl', class_='work_spec_list')
                spec_list = BeautifulSoup(requests.get(dlsite_site_url).text, 'lxml').find('table', id='work_outline')
                _mb = re.search(r'([0-9]+\.[0-9]+)MB\n', spec_list.get_text())
                if _mb is None:
                    dlsite_size = 0

                    # GB表記の処理
                    _gb = re.search(r'([0-9]+\.[0-9]+)GB', spec_list.get_text())
                    if _gb is not None:
                        dlsite_size = float(_gb.group(1))*1024

                else:
                    dlsite_size = float(_mb.group(1))
                print('dlsite_size: ' + str(dlsite_size))

                dlsite_amino_price = dlsite_price
                if dlsite_size != 0:
                    dlsite_amino_price = math.ceil(dlsite_price/dlsite_size)
                print('dlsite_amino_price: ' + str(dlsite_amino_price))
                print('')
                print('')


                item=Item.objects.update_or_create(site_url=dlsite_site_url, defaults={'title': dlsite_title, 'image_url': dlsite_image_url, 'site_url': dlsite_site_url, 'description_text': dlsite_description_text, 'amino_price': dlsite_amino_price, 'price': dlsite_price, 'distributor': 'dlsite', 'size': dlsite_size, 'discount_rate': dlsite_discount_rate, 'period_at': dlsite_period_at, 'item_type': Item.ItemType.XXX_BOOK})


