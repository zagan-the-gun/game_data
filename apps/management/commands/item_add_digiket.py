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

        print('digiket.comからJSONでエロゲ商品情報取得')
        #digiket_url = 'https://api.digiket.com/xml/api/getxml.php?target=4&sort=new&A=%25OFF&ie=UTF-8&xmltype=JSON'
        #digiket_json = json.loads(requests.get(digiket_url).text)
        digiket_url = 'https://www.digiket.com/a/result/_data/A=%93%AF%90l%83Q%81%5B%83%80/view=list/camp=on/sort=week/'

        cookie = {'adult_check': '1'}
        soup = BeautifulSoup(requests.get(digiket_url, cookies=cookie).text, 'lxml')

        for i in soup.find_all('div', class_='item-box'):
            digiket_site_url        = 'https://www.digiket.com' + i.find('a').get('href') + 'AFID=zagan/'
            print('digiket_site_url: ' + str(digiket_site_url))

            digiket_discount_rate   = re.search(r'([0-9]+)', i.find('span', class_='item-title_prcent').get_text()).group(1)
            print('digiket_discount_rate: ' + str(digiket_discount_rate))

            _pd                     = re.search(r'([0-9]+月[0-9]+日)', i.find('div', class_='discount').get_text())
            digiket_period_at = pytz.timezone('Asia/Tokyo').localize(datetime.datetime.strptime('2020年' + _pd.group(1) + ' 23:59:59', '%Y年%m月%d日 %H:%M:%S'))
            print('digiket_period_at: ' + str(  digiket_period_at))

            digiket_title           = i.find('dt', class_='item_name').find('a').get_text()
            print('digiket_title: ' + digiket_title)

            digiket_price           = re.search(r'([0-9]+)円', i.find('dt', class_='item-price-box').find('strong').get_text()).group(1)
            print('digiket_price: ' + str(digiket_price))

            # amino_priceを求める
            detail_url = digiket_site_url
            cookie = {'adult_check': '1'}
            _text = requests.get(digiket_site_url, cookies=cookie).text

            _b = re.search(r'ファイル容量：</div><div class="sub-data2">([0-9.,]+)?\s*byte', _text)
            b = int(_b.group(1).replace(',', ''))
            digiket_size = math.ceil((b/1024)/1024)
            print('digiket_size: ' + str(digiket_size))

            digiket_amino_price = math.ceil(int(digiket_price)/digiket_size)
            print('digiket_amino_price: ' + str(digiket_amino_price))

            digiket_image_url = BeautifulSoup(_text, 'lxml').find('div', class_='item').find('img').get('src')
            print('digiket_image_url: ' + digiket_image_url)

            digiket_original_price = re.search(r'([0-9]+)円', i.find('dt', class_='item-price-box').find('s').get_text()).group(1)
            print('digiket_original_price: ' + str(digiket_original_price))

            digiket_description_text = i.find('dd', class_='item_intro').get_text()
            print('digiket_description_text: ' + str(digiket_description_text))
            print('')
            print('')

            item=Item.objects.update_or_create(site_url=digiket_site_url, defaults={'title': digiket_title, 'image_url': digiket_image_url, 'site_url': digiket_site_url, 'description_text': digiket_description_text, 'amino_price': digiket_amino_price, 'price': digiket_price, 'original_price': digiket_original_price, 'distributor': 'digiket', 'size': digiket_size, 'discount_rate': digiket_discount_rate, 'period_at': digiket_period_at, 'item_type': Item.ItemType.XXX_GAME})


        print('digiket.comからJSONでエロ本商品情報取得')
        #digiket_url = 'https://www.digiket.com/a/result/_data/A=%93%AF%90l%83Q%81%5B%83%80/view=list/camp=on/sort=week/'
        digiket_url = 'https://www.digiket.com/a/result/_data/genre=%83R%83~%83b%83N/view=list/limit=30/camp=on/sort=week/'

        cookie = {'adult_check': '1'}
        soup = BeautifulSoup(requests.get(digiket_url, cookies=cookie).text, 'lxml')

        for i in soup.find_all('div', class_='item-box'):
            digiket_site_url        = 'https://www.digiket.com' + i.find('a').get('href') + 'AFID=zagan/'
            print('digiket_site_url: ' + str(digiket_site_url))

            digiket_discount_rate   = re.search(r'([0-9]+)', i.find('span', class_='item-title_prcent').get_text()).group(1)
            print('digiket_discount_rate: ' + str(digiket_discount_rate))

            _pd                     = re.search(r'([0-9]+月[0-9]+日)', i.find('div', class_='discount').get_text())
            digiket_period_at = pytz.timezone('Asia/Tokyo').localize(datetime.datetime.strptime('2020年' + _pd.group(1) + ' 23:59:59', '%Y年%m月%d日 %H:%M:%S'))
            print('digiket_period_at: ' + str(  digiket_period_at))

            digiket_title           = i.find('dt', class_='item_name').find('a').get_text()
            print('digiket_title: ' + digiket_title)

            digiket_price           = re.search(r'([0-9]+)円', i.find('dt', class_='item-price-box').find('strong').get_text()).group(1)
            print('digiket_price: ' + str(digiket_price))

            # amino_priceを求める
            detail_url = digiket_site_url
            cookie = {'adult_check': '1'}
            _text = requests.get(digiket_site_url, cookies=cookie).text

            _b = re.search(r'ファイル容量：</div><div class="sub-data2">([0-9.,]+)?\s*byte', _text)
            b = int(_b.group(1).replace(',', ''))
            digiket_size = math.ceil((b/1024)/1024)
            print('digiket_size: ' + str(digiket_size))

            digiket_amino_price = math.ceil(int(digiket_price)/digiket_size)
            print('digiket_amino_price: ' + str(digiket_amino_price))

            digiket_image_url = BeautifulSoup(_text, 'lxml').find('div', class_='item').find('img').get('src')
            print('digiket_image_url: ' + digiket_image_url)

            digiket_original_price = re.search(r'([0-9]+)円', i.find('dt', class_='item-price-box').find('s').get_text()).group(1)
            print('digiket_original_price: ' + str(digiket_original_price))

            digiket_description_text = i.find('dd', class_='item_intro').get_text()
            print('digiket_description_text: ' + str(digiket_description_text))
            print('')
            print('')

            item=Item.objects.update_or_create(site_url=digiket_site_url, defaults={'title': digiket_title, 'image_url': digiket_image_url, 'site_url': digiket_site_url, 'description_text': digiket_description_text, 'amino_price': digiket_amino_price, 'price': digiket_price, 'original_price': digiket_original_price, 'distributor': 'digiket', 'size': digiket_size, 'discount_rate': digiket_discount_rate, 'period_at': digiket_period_at, 'item_type': Item.ItemType.XXX_BOOK})

