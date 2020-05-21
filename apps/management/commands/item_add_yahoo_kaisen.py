from django.core.management import BaseCommand
from ...models import Item

import json
import requests
import re

import math

import urllib.parse


class Command(BaseCommand):
    help = 'カニ情報収集'

#    def add_arguments(self, parser):
#        parser.add_argument('-c', '--command', dest='command', help='add or del')
#        parser.add_argument('opt1', help='必須オプション')
#        parser.add_argument('--opt2', help='任意オプション')
#        parser.add_argument('--date', help='何日前')
 
    def handle(self, *args, **options):
#        print(options['command'])
        self.stdout.write(self.style.SUCCESS('DEBUG DEBUG DEBUG item_add: '))
#        self.stdout.write(options.__str__())


        find_list=[]
        find_list.append({'item_type': Item.ItemType.KAISEN_KANI, 'text': 'カニ 送料無料'})
        find_list.append({'item_type': Item.ItemType.KAISEN_KANI, 'text': 'カニ 訳あり 送料無料'})

        find_list.append({'item_type': Item.ItemType.KAISEN_EBI, 'text': 'エビ 送料無料'})

        find_list.append({'item_type': Item.ItemType.KAISEN_KAKI, 'text': '牡蠣'})
        find_list.append({'item_type': Item.ItemType.KAISEN_KAKI, 'text': '牡蠣 送料無料'})
        for fl in find_list:
            fl_url = urllib.parse.quote(fl['text'])
            print('種別: {} 検索文字列: {}'.format(fl['item_type'].label, fl['text']))

            # Yahoo!からJSONで商品情報取得
            yahoo_url = 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/itemSearch?appid=dj00aiZpPWVwMENvd0dOUUxzZiZzPWNvbnN1bWVyc2VjcmV0Jng9M2Y-&affiliate_type=vc&affiliate_id=http%3A%2F%2Fck.jp.ap.valuecommerce.com%2Fservlet%2Freferral%3Fsid%3D3519741%26pid%3D886480311%26vc_url%3D&query=' + fl_url
            yahoo_json = json.loads(requests.get(yahoo_url).text)
 
            #for y in yahoo_json['ResultSet']['0']['Result'].items():
            for y in yahoo_json['ResultSet']['0']['Result'].values():
                if (y not in ['Request', 'Modules', '_container', 'Hit', '']) and ('Query' not in y):
                    y_title            = y['Name']
                    y_image_url        = y['Image']['Medium']
                    y_site_url         = y['Url']
                    y_description_text = y['Description']
                    y_price            = int(y['Price']['_value'])

                    y_amino_price       = int(y['Price']['_value'])
                    # タイトルから重量取得
                    #for i in sorted(re.findall(r'([0-9]+)g', y_title), key=int, reverse=True):
                    for i in sorted(re.findall(r'([0-9]+)g', y_title), key=int):
                        # 一番小さい数字を使って割る
                        if int(i) > 1:
                            y_amino_price=math.ceil(y_price/(int(i)/100))
                            break

                    # 取得できなかったらkgでサーチ
                    if y_amino_price == y_price:
                        #for i in sorted(re.findall(r'([0-9]+.[0-9]+|[0-9]+)kg', y_title), key=float, reverse=True):
                        for i in sorted(re.findall(r'([0-9]+\.[0-9]+|[0-9]+)kg', y_title), key=float):
                            if float(i) > 0:
                                y_amino_price=math.ceil(y_price/((float(i)*1000)/100))
                                break

    #                # descriptionから重量取得(誤集計多いので保留)
    #                if y_amino_price == y_price:
    #                    for i in sorted(re.findall(r'([0-9]+)枚', r_description_text), key=int, reverse=True):
    #                        if int(i) > 1:
    #                            y_amino_price=math.ceil(y_price/int(i))
    #                            break

                    # 単価が取得できなければDBに入れない
                    if y_amino_price == y_price:
                        continue

                    # 送料チェック
                    y_shipping_price=None
                    if int(y['Shipping']['Code']) == 2:
                        y_shipping_price=0

                    Item.objects.update_or_create(site_url=y_site_url, defaults={'title': y_title, 'image_url': y_image_url, 'site_url': y_site_url, 'description_text': y_description_text, 'amino_price': y_amino_price, 'price': y_price, 'distributor': 'yahoo', 'shipping_price': y_shipping_price, 'item_type': fl['item_type']})

        """
        # Yahoo!からJSONでエビ商品情報取得
        #エビ 送料無料
        yahoo_url = 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/itemSearch?appid=dj00aiZpPWVwMENvd0dOUUxzZiZzPWNvbnN1bWVyc2VjcmV0Jng9M2Y-&affiliate_type=vc&affiliate_id=http%3A%2F%2Fck.jp.ap.valuecommerce.com%2Fservlet%2Freferral%3Fsid%3D3519741%26pid%3D886480311%26vc_url%3D&query=%E3%82%A8%E3%83%93%20%E9%80%81%E6%96%99%E7%84%A1%E6%96%99'
        yahoo_json = json.loads(requests.get(yahoo_url).text)
 
        #for y in yahoo_json['ResultSet']['0']['Result'].items():
        for y in yahoo_json['ResultSet']['0']['Result'].values():
            if (y not in ['Request', 'Modules', '_container', 'Hit', '']) and ('Query' not in y):
                y_title            = y['Name']
                y_image_url        = y['Image']['Medium']
                y_site_url         = y['Url']
                y_description_text = y['Description']
                y_price            = int(y['Price']['_value'])

                y_amino_price       = int(y['Price']['_value'])
                # タイトルから重量取得
                #for i in sorted(re.findall(r'([0-9]+)g', y_title), key=int, reverse=True):
                for i in sorted(re.findall(r'([0-9]+)g', y_title), key=int):
                    # 一番小さい数字を使って割る
                    if int(i) > 1:
                        y_amino_price=math.ceil(y_price/(int(i)/100))
                        break

             # 取得できなかったらkgでサーチ
                if y_amino_price == y_price:
                    #for i in sorted(re.findall(r'([0-9]+.[0-9]+|[0-9]+)kg', y_title), key=float, reverse=True):
                    for i in sorted(re.findall(r'([0-9]+.[0-9]+|[0-9]+)kg', y_title), key=float):
                        if float(i) > 0:
                            y_amino_price=math.ceil(y_price/((float(i)*1000)/100))
                            break

#                # descriptionから重量取得(誤集計多いので保留)
#                if y_amino_price == y_price:
#                    for i in sorted(re.findall(r'([0-9]+)枚', r_description_text), key=int, reverse=True):
#                        if int(i) > 1:
#                            y_amino_price=math.ceil(y_price/int(i))
#                            break

                # 単価が取得できなければDBに入れない
                if y_amino_price == y_price:
                    continue

                # 送料チェック
                y_shipping_price=None
                if int(y['Shipping']['Code']) == 2:
                    y_shipping_price=0

                Item.objects.update_or_create(site_url=y_site_url, defaults={'title': y_title, 'image_url': y_image_url, 'site_url': y_site_url, 'description_text': y_description_text, 'amino_price': y_amino_price, 'price': y_price, 'distributor': 'yahoo', 'shipping_price': y_shipping_price, 'item_type': Item.ItemType.KAISEN_EBI})


        # Yahoo!からJSONでカキ商品情報取得
        #牡蠣
        yahoo_url = 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/itemSearch?appid=dj00aiZpPWVwMENvd0dOUUxzZiZzPWNvbnN1bWVyc2VjcmV0Jng9M2Y-&affiliate_type=vc&affiliate_id=http%3A%2F%2Fck.jp.ap.valuecommerce.com%2Fservlet%2Freferral%3Fsid%3D3519741%26pid%3D886480311%26vc_url%3D&query=%E7%89%A1%E8%A0%A3'
        #牡蠣 訳あり 送料無料
        #yahoo_url = 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/itemSearch?appid=dj00aiZpPWVwMENvd0dOUUxzZiZzPWNvbnN1bWVyc2VjcmV0Jng9M2Y-&affiliate_type=vc&affiliate_id=http%3A%2F%2Fck.jp.ap.valuecommerce.com%2Fservlet%2Freferral%3Fsid%3D3519741%26pid%3D886480311%26vc_url%3D&query=%E7%89%A1%E8%A0%A3%20%E8%A8%B3%E3%81%82%E3%82%8A%20%E9%80%81%E6%96%99%E7%84%A1%E6%96%99'
        yahoo_json = json.loads(requests.get(yahoo_url).text)
 
        for y in yahoo_json['ResultSet']['0']['Result'].values():
            if (y not in ['Request', 'Modules', '_container', 'Hit', '']) and ('Query' not in y):
                y_title            = y['Name']
                y_image_url        = y['Image']['Medium']
                y_site_url         = y['Url']
                y_description_text = y['Description']
                y_price            = int(y['Price']['_value'])

                y_amino_price       = int(y['Price']['_value'])
                # タイトルから重量取得
                for i in sorted(re.findall(r'([0-9]+)g', y_title), key=int):
                    # 一番小さい数字を使って割る
                    if int(i) > 1:
                        y_amino_price=math.ceil(y_price/(int(i)/100))
                        break

             # 取得できなかったらkgでサーチ
                if y_amino_price == y_price:
                    for i in sorted(re.findall(r'([0-9]+.[0-9]+|[0-9]+)kg', y_title), key=float):
                        if float(i) > 0:
                            y_amino_price=math.ceil(y_price/((float(i)*1000)/100))
                            break

#                # descriptionから重量取得(誤集計多いので保留)
#                if y_amino_price == y_price:
#                    for i in sorted(re.findall(r'([0-9]+)枚', r_description_text), key=int, reverse=True):
#                        if int(i) > 1:
#                            y_amino_price=math.ceil(y_price/int(i))
#                            break

                # 単価が取得できなければDBに入れない
                if y_amino_price == y_price:
                    continue

                # 送料チェック
                y_shipping_price=None
                if int(y['Shipping']['Code']) == 2:
                    y_shipping_price=0

                Item.objects.update_or_create(site_url=y_site_url, defaults={'title': y_title, 'image_url': y_image_url, 'site_url': y_site_url, 'description_text': y_description_text, 'amino_price': y_amino_price, 'price': y_price, 'distributor': 'yahoo', 'shipping_price': y_shipping_price, 'item_type': Item.ItemType.KAISEN_KAKI})

        """
