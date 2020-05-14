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
        digiket_url = 'https://api.digiket.com/xml/api/getxml.php?target=4&sort=new&A=%25OFF&ie=UTF-8&xmltype=JSON'
        digiket_json = json.loads(requests.get(digiket_url).text)

        for d in digiket_json:

            digiket_title            = d['trade_name_raw']
            digiket_image_url        = d['trade_cg_1']
            digiket_site_url         = d['url']
            digiket_description_text = d['intro']
            digiket_price            = d['price']
            digiket_amino_price      = d['price']

            # amino_priceを求める
            detail_url = digiket_site_url
            cookie = {'adult_check': '1'}

            _b = re.search(r'ファイル容量：</div><div class="sub-data2">([0-9.,]+)?\s*byte', requests.get(digiket_site_url, cookies=cookie).text)
            b = int(_b.group(1).replace(',', ''))
            mb = math.ceil((b/1024)/1024)
            digiket_amino_price = math.ceil(int(digiket_price)/mb)

#            print('digiket_site_url: ' + digiket_site_url)
#            print('digiket_price: ' + digiket_price)
#            print('digiket_amino_price' + str(digiket_amino_price))
#            print('')

            item=Item.objects.update_or_create(site_url=digiket_site_url, defaults={'title': digiket_title, 'image_url': digiket_image_url, 'site_url': digiket_site_url, 'description_text': digiket_description_text, 'amino_price': digiket_amino_price, 'price': digiket_price, 'distributor': 'digiket', 'item_type': Item.ItemType.XXX_GAME})
        print('add: ' + str(len(digiket_json)))


        print('digiket.comからJSONでエロ本商品情報取得')
        digiket_url = 'https://api.digiket.com/xml/api/getxml.php?target=5&sort=new&A=%25OFF&ie=UTF-8&xmltype=JSON'
        digiket_json = json.loads(requests.get(digiket_url).text)

        for d in digiket_json:

            digiket_title            = d['trade_name_raw']
            digiket_image_url        = d['trade_cg_1']
            digiket_site_url         = d['url']
            digiket_description_text = d['intro']
            digiket_price            = d['price']
            digiket_amino_price      = d['price']

            # amino_priceを求める
            # ページの前にある数字を取得
            detail_url = digiket_site_url
            cookie = {'adult_check': '1'}
            for i in sorted(re.findall(r'([0-9]+)ページ', requests.get(digiket_site_url, cookies=cookie).text), key=int, reverse=True):
                if int(i) > 1:
                    digiket_amino_price = math.ceil(int(digiket_price)/int(i))
#                    print('page: ' + i)
                    break

#            print('digiket_site_url: ' + digiket_site_url)
#            print('digiket_price: ' + digiket_price)
#            print('digiket_amino_price: ' + str(digiket_amino_price))
#            print('')

            item=Item.objects.update_or_create(site_url=digiket_site_url, defaults={'title': digiket_title, 'image_url': digiket_image_url, 'site_url': digiket_site_url, 'description_text': digiket_description_text, 'amino_price': digiket_amino_price, 'price': digiket_price, 'distributor': 'digiket', 'item_type': Item.ItemType.XXX_BOOK})
        print('add: ' + str(len(digiket_json)))

