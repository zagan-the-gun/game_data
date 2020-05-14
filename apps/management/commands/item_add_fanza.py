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


        print('fanzaからJSONでエロ本商品情報取得')
        fanza_url = 'https://www.dmm.co.jp/dc/doujin/-/list/=/campaign=gain/sort=review_rank/'
        cookie = {'adult_check': '1'}
        soup = BeautifulSoup(requests.get(fanza_url, cookies=cookie).text, 'lxml')

        for li in soup.find_all('li', class_='productList__item',):
            if li.find('div', class_='listGenreIco__ico').get_text() in ['コミック', 'ＣＧ']:
                print(li.find('div', class_='listGenreIco__ico').get_text())

                fanza_site_url = 'https://www.dmm.co.jp' + li.find('div', class_='tileListImg__tmb').find('a').get('href')
                print('fanza_site_url: ' + fanza_site_url)

                # スクレイピング開始
                detail_url = fanza_site_url #不要？
                cookie = {'adult_check': '1'}
                site_content = requests.get(fanza_site_url, cookies=cookie).text
                site_soup = BeautifulSoup(site_content, 'lxml')

                # titlenを取得
                fanza_title = site_soup.find('meta', property='og:title').get('content')
                print('fanza_title: ' + fanza_title)

                # discount_rateを取得
                _d = re.search(r'([0-9]+)%OFF', site_soup.find('p', class_='campaignBalloon__ttl').get_text())
                fanza_discount_rate = _d.group(1)
                print('fanza_discount_rate: ' + str(fanza_discount_rate))

                # descriptionを取得
                fanza_description_text = re.sub('          ', '', site_soup.find('p', class_='summary__txt').get_text() )
#                print('fanza_description: ' + fanza_description_text)

                # priceを取得
                _p = re.search(r'([0-9.,]+)', site_soup.find('p', class_='priceList__main priceList__main--emphasis').get_text())
                fanza_price = int(_p.group(1).replace(',', ''))
                print('fanza_price: ' + str(fanza_price))

                # amino_priceを求める
                _mb = re.search(r'([0-9]+\.[0-9]+)MB', site_soup.find('div', class_='productInformation u-common__clearfix').get_text())
                if _mb is not None:
                    fanza_size = math.ceil(float(_mb.group(1)))
                    fanza_amino_price = math.ceil(int(fanza_price)/fanza_size)
                else:
                    fanza_size = 0
                    fanza_amino_price = int(fanza_price)
                print('fanza_amino_price: ' + str(fanza_amino_price))
                print('fanza_size: ' + str(fanza_size))

                # period_atを取得
                _pd = re.search(r'\s+(.*日)\s', site_soup.find('p', class_='campaignBalloon__txt').get_text())
                #fanza_period_at = datetime.datetime.strptime(_pd.group(1), '%Y年%m月%d日').replace(tzinfo=pytz.timezone('Asia/Tokyo'))
                fanza_period_at = pytz.timezone('Asia/Tokyo').localize(datetime.datetime.strptime(_pd.group(1) + ' 23:59:59', '%Y年%m月%d日 %H:%M:%S'))
                print('fanza_period_at: ' + str(fanza_period_at))

                # titlenを取得
                #fanza_image_url = site_soup.find('li', class_='productPreview__item', style='display: table;').find('img').get('src')
                fanza_image_url = site_soup.find('ul', class_='productPreview').find('a').get('href')
                print('fanza_image_url: ' + fanza_image_url)


                print('')
                print('')

                item=Item.objects.update_or_create(site_url=fanza_site_url, defaults={'title': fanza_title, 'image_url': fanza_image_url, 'site_url': fanza_site_url, 'description_text': fanza_description_text, 'amino_price': fanza_amino_price, 'price': fanza_price, 'distributor': 'fanza', 'size': fanza_size, 'discount_rate': fanza_discount_rate, 'period_at': fanza_period_at, 'item_type': Item.ItemType.XXX_BOOK})


        print('fanzaからJSONでエロゲ商品情報取得')
        fanza_url = 'https://www.dmm.co.jp/dc/doujin/-/list/narrow/=/campaign=gain/n1=AgReSwMKX1VZCFQCloTHi8SF/sort=review_rank/'
        cookie = {'adult_check': '1'}
        soup = BeautifulSoup(requests.get(fanza_url, cookies=cookie).text, 'lxml')

        for li in soup.find_all('li', class_='productList__item',):
            if li.find('div', class_='listGenreIco__ico').get_text() in ['ゲーム']:
                print(li.find('div', class_='listGenreIco__ico').get_text())

                fanza_site_url = 'https://www.dmm.co.jp' + li.find('div', class_='tileListImg__tmb').find('a').get('href')
                print('fanza_site_url: ' + fanza_site_url)

                # スクレイピング開始
                detail_url = fanza_site_url #不要？
                cookie = {'adult_check': '1'}
                site_content = requests.get(fanza_site_url, cookies=cookie).text
                site_soup = BeautifulSoup(site_content, 'lxml')

                # titlenを取得
                fanza_title = site_soup.find('meta', property='og:title').get('content')
                print('fanza_title: ' + fanza_title)

                # discount_rateを取得
                _d = re.search(r'([0-9]+)%OFF', site_soup.find('p', class_='campaignBalloon__ttl').get_text())
                fanza_discount_rate = _d.group(1)
                print('fanza_discount_rate: ' + str(fanza_discount_rate))

                # descriptionを取得
                fanza_description_text = re.sub('          ', '', site_soup.find('p', class_='summary__txt').get_text() )
#                print('fanza_description: ' + fanza_description_text)

                # priceを取得
                _p = re.search(r'([0-9.,]+)', site_soup.find('p', class_='priceList__main priceList__main--emphasis').get_text())
                fanza_price = int(_p.group(1).replace(',', ''))
                print('fanza_price: ' + str(fanza_price))

                # amino_priceを求める
                _mb = re.search(r'([0-9]+\.[0-9]+)MB', site_soup.find('div', class_='productInformation u-common__clearfix').get_text())
                if _mb is not None:
                    fanza_size = math.ceil(float(_mb.group(1)))
                    fanza_amino_price = math.ceil(int(fanza_price)/fanza_size)
                else:
                    fanza_size = 0
                    fanza_amino_price = int(fanza_price)
                print('fanza_amino_price: ' + str(fanza_amino_price))
                print('fanza_size: ' + str(fanza_size))

                # period_atを取得
                _pd = re.search(r'\s+(.*日)\s', site_soup.find('p', class_='campaignBalloon__txt').get_text())
                #fanza_period_at = datetime.datetime.strptime(_pd.group(1), '%Y年%m月%d日').replace(tzinfo=pytz.timezone('Asia/Tokyo'))
                fanza_period_at = pytz.timezone('Asia/Tokyo').localize(datetime.datetime.strptime(_pd.group(1) + ' 23:59:59', '%Y年%m月%d日 %H:%M:%S'))
                print('fanza_period_at: ' + str(fanza_period_at))

                # titlenを取得
                #fanza_image_url = site_soup.find('li', class_='productPreview__item', style='display: table;').find('img').get('src')
                fanza_image_url = site_soup.find('ul', class_='productPreview').find('a').get('href')
                print('fanza_image_url: ' + fanza_image_url)


                print('')
                print('')

                item=Item.objects.update_or_create(site_url=fanza_site_url, defaults={'title': fanza_title, 'image_url': fanza_image_url, 'site_url': fanza_site_url, 'description_text': fanza_description_text, 'amino_price': fanza_amino_price, 'price': fanza_price, 'distributor': 'fanza', 'size': fanza_size, 'discount_rate': fanza_discount_rate, 'period_at': fanza_period_at, 'item_type': Item.ItemType.XXX_GAME})

