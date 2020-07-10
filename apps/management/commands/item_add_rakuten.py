from django.core.management import BaseCommand
from ...models import Item, SearchWord, ItemType

import json
import requests
import re

import math

import urllib.parse


class Command(BaseCommand):
    help = '楽天情報収集'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('DEBUG DEBUG DEBUG item_add: '))

        find_list=[]
        search_word = SearchWord.objects.all()
        for sw in search_word:
            find_list.append({'text': sw.word, 'tags': u", ".join(s.name for s in sw.tags.all())})

        for fl in find_list:
            fl_url = urllib.parse.quote(fl['text'])
            print('タグ: {} 検索文字列: {}'.format(fl['tags'], fl['text']))

            # 楽天からJSONで商品情報取得
            rakuten_url = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?format=json&keyword=' + fl_url + '&affiliateId=1b221d9c.03487084.1b221d9d.56b5e1b5&applicationId=1040781665970884363'
            rakuten_json = json.loads(requests.get(rakuten_url).text)

            for r in rakuten_json['Items']:

                r_title            = r['Item']['itemName']
                r_image_url        = r['Item']['mediumImageUrls'][0]['imageUrl']
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

                # 送料チェック
                r_shipping_price=None
                if '送料無料' in r_title:
                    r_shipping_price=0

                print(fl['tags'])
                print(type(fl['tags']))
                Item.objects.update_or_create(site_url=r_site_url, defaults={'title': r_title, 'image_url': r_image_url, 'site_url': r_site_url, 'description_text': r_description_text, 'amino_price': r_amino_price, 'price': r_price, 'distributor': 'rakuten', 'shipping_price': r_shipping_price, })
                item = Item.objects.get(site_url=r_site_url)
                item.tags.add(fl['tags'])

