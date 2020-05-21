from django.core.management import BaseCommand
from ...models import Item

import json
import requests
import re

import math

import urllib.parse


class Command(BaseCommand):
    help = '楽天海鮮情報収集'

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

            # 楽天からJSONで商品情報取得
            rakuten_url = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?format=json&keyword=' + fl_url + '&affiliateId=1b221d9c.03487084.1b221d9d.56b5e1b5&applicationId=1040781665970884363'
            rakuten_json = json.loads(requests.get(rakuten_url).text)

            for r in rakuten_json['Items']:

                r_title            = r['Item']['itemName']
                r_image_url        = r['Item']['mediumImageUrls'][0]['imageUrl']
                #r_site_url         = r['Item']['itemUrl']
                r_site_url         = r['Item']['affiliateUrl']
                r_description_text = r['Item']['itemCaption']
                r_price            = r['Item']['itemPrice']

                r_amino_price       = r['Item']['itemPrice']
                print(r_title)
                print(r_price)
                # タイトルから重量取得
                for i in sorted(re.findall(r'([0-9]+)g', r_title), key=int):
                    # 一番小さい数字を使って割る
                    if int(i) > 1:
                        print(i)
                        r_amino_price=math.ceil(r_price/(int(i)/100))
                        break

                # 取得できなかったらkgでサーチ
                if r_amino_price == r_price:
                    for i in sorted(re.findall(r'([0-9]+\.[0-9]+|[0-9]+)kg', r_title.replace(',', '.')), key=float):
                        if float(i) > 0:
                            print(i)
                            r_amino_price=math.ceil(r_price/((float(i)*1000)/100))
                            break

                # 単価が取得できなければDBに入れない
                if r_amino_price == r_price:
                    continue
                print(r_amino_price)
                print('')
                print('')

                # descriptionから重量取得(誤集計多いので保留)
    #            if r_amino_price == r_price:
    #                for i in sorted(re.findall(r'([0-9]+)枚', r_description_text), key=int, reverse=True):
    #                    if int(i) > 1:
    #                        r_amino_price=math.ceil(r_price/int(i))
    #                        break

                # 送料チェック
                r_shipping_price=None
                if '送料無料' in r_title:
                    r_shipping_price=0

                item=Item.objects.update_or_create(site_url=r_site_url, defaults={'title': r_title, 'image_url': r_image_url, 'site_url': r_site_url, 'description_text': r_description_text, 'amino_price': r_amino_price, 'price': r_price, 'distributor': 'rakuten', 'shipping_price': r_shipping_price, 'item_type': fl['item_type']})

