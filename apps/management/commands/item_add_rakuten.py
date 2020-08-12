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
            # 検索対象判別
            if (sw.distributor == 1) or (sw.distributor == 2):
                find_list.append({'text': sw.word, 'tags': sw.tags.all(), 'notation_unit': sw.notation_unit, 'exclusion_word': sw.exclusion_word})

        for fl in find_list:

            fl_url = urllib.parse.quote(fl['text'])
            print('タグ: {} 検索文字列: {}'.format(u", ".join(s.name for s in fl['tags']), fl['text']))

            # 楽天からJSONで商品情報取得
            rakuten_url = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?format=json&keyword=' + fl_url + '&affiliateId=1b221d9c.03487084.1b221d9d.56b5e1b5&applicationId=1040781665970884363'
            rakuten_json = json.loads(requests.get(rakuten_url).text)

            for r in rakuten_json['Items']:
                # 除外ワードのスキップ処理
                exclusion_word = fl['exclusion_word'] or ''
                for ew in exclusion_word.split(' '):
                    if (ew or 'asdf') in r['Item']['itemName']:
                        print('DEBUG DEBUG DEBUG exclusion_word HIT!: ')
                        print(ew)
                        print(r['Item']['itemName'])
                        continue
                for ew in exclusion_word.split(' '):
                    if ( ew or 'asdf') in r['Item']['itemCaption']:
                        print('DEBUG DEBUG DEBUG exclusion_word HIT!: ')
                        print(ew)
                        print(r['Item']['itemCaption'])
                        continue

                r_title            = r['Item']['itemName']
                r_image_url        = r['Item']['mediumImageUrls'][0]['imageUrl']
                r_site_url         = r['Item']['affiliateUrl']
                r_description_text = r['Item']['itemCaption']
                r_price            = r['Item']['itemPrice']

                r_amino_price       = r['Item']['itemPrice']
#                print(r_title)
#                print(r_price)
#                print('単位' + fl['notation_unit'])
                if fl['notation_unit'] == 'g':
                    # タイトルから重量取得
                    for i in sorted(re.findall(r'([0-9]+)g', r_title), key=int):
                        # 一番小さい数字を使って割る
                        if int(i) > 1:
#                            print(i)
                            r_amino_price=math.ceil(r_price/(int(i)/100))
                            break
                    # 取得できなかったらkgでサーチ
                    if r_amino_price == r_price:
                        for i in sorted(re.findall(r'([0-9]+\.[0-9]+|[0-9]+)kg', r_title.replace(',', '.')), key=float):
                            if float(i) > 0:
#                                print(i)
                                r_amino_price=math.ceil(r_price/((float(i)*1000)/100))
                                break

                elif fl['notation_unit'] == 'ml':
                    # mlの前にある数字を全部集める
                    for i in sorted(re.findall(r'([0-9]+)ml', r_title), key=int):
                        if int(i) > 1:
                            r_amino_price=math.ceil(r_price/(int(i)/100))
                            break
                    # 業務用はL表示なので合わせる
                    if r_amino_price == r_price:
                        for i in sorted(re.findall(r'([0-9]+)L', r_title), key=int):
                            if int(i) > 1:
                                r_amino_price=math.ceil(r_price/((float(i)*1000)/100))
                                break

                elif fl['notation_unit'] == '枚':
                    # 枚の前にある数字を全部集める
                    for i in sorted(re.findall(r'([0-9]+)枚', r_title), key=int, reverse=True):
                        if int(i) > 1:
                            r_amino_price=math.ceil(r_price/int(i))
                            break
                    # デスクリプション
                    if r_amino_price == r_price:
                        for i in sorted(re.findall(r'([0-9]+)枚', r_description_text), key=int, reverse=True):
                            if int(i) > 1:
                                r_amino_price=math.ceil(r_price/int(i))
                                break

                # 単価が取得できなければDBに入れない
                if r_amino_price == r_price:
                    continue
#                print(r_amino_price)
#                print('')
#                print('')

                # 送料チェック
                r_shipping_price=None
                if '送料無料' in r_title:
                    r_shipping_price=0

#                print(fl['tags'])
                Item.objects.update_or_create(site_url=r_site_url, defaults={'title': r_title, 'image_url': r_image_url, 'site_url': r_site_url, 'description_text': r_description_text, 'amino_price': r_amino_price, 'price': r_price, 'distributor': 'rakuten', 'shipping_price': r_shipping_price, })
                item = Item.objects.get(site_url=r_site_url)
                for tag in fl['tags']:
                    item.tags.add(tag)

