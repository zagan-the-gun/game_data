from django.core.management import BaseCommand
from ...models import Item, SearchWord, ItemType

import json
import requests
import re

import math

import urllib.parse


class Command(BaseCommand):
    help = 'Yahoo情報収集'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('DEBUG DEBUG DEBUG item_add: '))

        find_list=[]
        search_word = SearchWord.objects.all()
        for sw in search_word:
            find_list.append({'text': sw.word, 'tags': u", ".join(s.name for s in sw.tags.all()), 'notation_unit': sw.notation_unit, 'exclusion_word': sw.exclusion_word})

        for fl in find_list:
            fl_url = urllib.parse.quote(fl['text'])
            print('タグ: {} 検索文字列: {}'.format(fl['tags'], fl['text']))

            # Yahoo!からJSONで商品情報取得
            yahoo_url = 'https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch?appid=dj00aiZpPTh6NTZSUTFKcGlWSiZzPWNvbnN1bWVyc2VjcmV0Jng9NGU-&affiliate_type=vc&affiliate_id=http%3A%2F%2Fck.jp.ap.valuecommerce.com%2Fservlet%2Freferral%3Fsid%3D3519741%26pid%3D886480311%26vc_url%3D&in_stock=true&results=50&query=' + fl_url
            yahoo_json = json.loads(requests.get(yahoo_url).text)
 
            for y in yahoo_json['hits']:
                # 除外ワードのスキップ処理
                exclusion_word = fl['exclusion_word'] or ''
                for ew in exclusion_word.split(' '):
                    if (ew or 'asdf') in y['name']:
                        print('DEBUG DEBUG DEBUG exclusion_word HIT!: ')
                        print(ew)
                        print(y['name'])
                        continue
                for ew in exclusion_word.split(' '):
                    if ( ew or 'asdf') in y['description']:
                        print('DEBUG DEBUG DEBUG exclusion_word HIT!: ')
                        print(ew)
                        print(y['description'])
                        continue

                #新方式になってこのifは不要
                if (y not in ['Request', 'Modules', '_container', 'Hit', '']) and ('Query' not in y):
                    y_title            = y['name']
                    y_image_url        = y['image']['medium']
                    y_site_url         = y['url']
                    y_description_text = y['description']
                    y_price            = int(y['price'])
                    y_amino_price       = int(y['price'])

                    if fl['notation_unit'] == 'g':
                        # タイトルから重量取得
                        for i in sorted(re.findall(r'([0-9]+)g', y_title), key=int):
                            # 一番小さい数字を使って割る
                            if int(i) > 1:
                                y_amino_price=math.ceil(y_price/(int(i)/100))
                                break
                        # 取得できなかったらkgでサーチ
                        if y_amino_price == y_price:
                            for i in sorted(re.findall(r'([0-9]+\.[0-9]+|[0-9]+)kg', y_title), key=float):
                                if float(i) > 0:
                                    y_amino_price=math.ceil(y_price/((float(i)*1000)/100))
                                    break

                    elif fl['notation_unit'] == 'ml':
                        # mlの前にある数字を全部集める
                        for i in sorted(re.findall(r'([0-9]+)ml', y_title), key=int):
                            if int(i) > 1:
                                y_amino_price=math.ceil(y_price/(int(i)/100))
                                break
                        # 業務用はL表示なので合わせる
                        if y_amino_price != y_price:
                            for i in sorted(re.findall(r'([0-9]+)L', y_title), key=int):
                                if int(i) > 1:
                                    y_amino_price=math.ceil(y_price/((float(i)*1000)/100))
                                    break

                    elif fl['notation_unit'] == '枚':
                        # 枚の前にある数字を全部集める
                        for i in sorted(re.findall(r'([0-9]+)枚', y_title), key=int, reverse=True):
                            if int(i) > 1:
                                y_amino_price=math.ceil(y_price/int(i))
                                break

                    # 単価が取得できなければDBに入れない
                    if y_amino_price == y_price:
                        continue

                    # 送料チェック
                    y_shipping_price=None
                    if int(y['shipping']['code']) == 2:
                        y_shipping_price=0

                    Item.objects.update_or_create(site_url=y_site_url, defaults={'title': y_title, 'image_url': y_image_url, 'site_url': y_site_url, 'description_text': y_description_text, 'amino_price': y_amino_price, 'price': y_price, 'distributor': 'yahoo', 'shipping_price': y_shipping_price})
                    item = Item.objects.get(site_url=y_site_url)
                    item.tags.add(fl['tags'])

