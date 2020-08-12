from django.core.management import BaseCommand
from ...models import Item, SearchWord, ItemType

import re

import math

import urllib.parse

import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options



class Command(BaseCommand):
    help = '楽天情報収集'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('DEBUG DEBUG DEBUG item_add: '))


        START = datetime.datetime.now().timestamp()
        options = Options()
        # Google Chrome Canaryのインストールパスを指定する
        options.binary_location = '/usr/bin/google-chrome'
        # Headless Chromeを使うためのオプション
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument('--single-process')
#        options.add_argument('--disable-application-cache')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--start-maximized')
        options.add_argument("--dns-prefetch-disable") #効果が無いなら消す
        options.add_argument('--disable-extensions') #拡張機能無効
        options.add_argument('--proxy-server="direct://"') # Proxy経由ではなく直接接続する
        options.add_argument('--proxy-bypass-list=*')      # すべてのホスト名
#        options.add_argument("--remote-debugging-port=9222")#デバッグポート不要ならいらん

        find_list=[]
        #Todo ここに検索するかどうかの条件入れる
        search_word = SearchWord.objects.all()
        for sw in search_word:
            # 検索対象判別
            if (sw.distributor == 1) or (sw.distributor == 4):
                find_list.append({'text': sw.word, 'tags': sw.tags.all(), 'notation_unit': sw.notation_unit, 'exclusion_word': sw.exclusion_word})

        #for fl in find_list[0]:
        for fl in find_list:
            fl_url = urllib.parse.quote(fl['text'])
            print('タグ: {} 検索文字列: {}'.format(u", ".join(s.name for s in fl['tags']), fl['text']))

            START = datetime.datetime.now().timestamp()
            #driver = webdriver.Chrome(options=options, executable_path='venv3.8/lib/python3.8/site-packages/chromedriver_binary/chromedriver')
            driver = webdriver.Chrome(chrome_options=options, executable_path='venv3.8/lib/python3.8/site-packages/chromedriver_binary/chromedriver')
            print('open browser:{}s'.format(datetime.datetime.now().timestamp() - START))
            # Amazonから商品情報取得
            try:
                driver.get('https://www.amazon.co.jp/s?k=' + fl_url + '&ref=nb_sb_noss')
            except Exception as e:
                print('DEBUG DEBUG DEBUG driver.get() skip')
                driver.close()
                driver.quit()
                continue

            print('open top page:{}s'.format(datetime.datetime.now().timestamp() - START))
            soup = BeautifulSoup(driver.page_source, 'lxml')
            try:
                driver.close()
            except Exception as e:
                print('DEBUG DEBUG DEBUG driver.close() skip')
                driver.quit()
                continue

            print('close browser:{}s'.format(datetime.datetime.now().timestamp() - START))
            driver.quit()
            print('quit browser:{}s'.format(datetime.datetime.now().timestamp() - START))
            for div in soup.find_all('div', class_='s-asin',):

#                print(div)
                if div.find('span', class_='a-text-normal'):
                    a_title = div.find('span', class_='a-text-normal').get_text()
                else:
                    a_title = ''

                if div.find('span', class_='a-offscreen'):
                    _p = re.search(r'([0-9.,]+)', div.find('span', class_='a-offscreen').get_text())
                    a_price = int(_p.group(1).replace(',', ''))
                else:
                    a_price = 0

                a_amino_price = a_price

                # 除外ワードのスキップ処理
                exclusion_word = fl['exclusion_word'] or ''
                for ew in exclusion_word.split(' '):
                    if (ew or 'asdf') in a_title:
                        print('DEBUG DEBUG DEBUG exclusion_word HIT!: ')
                        print(ew)
                        print(a_title)
                        continue
#                for ew in exclusion_word.split(' '):
#                    if ( ew or 'asdf') in r['Item']['itemCaption']:
#                        print('DEBUG DEBUG DEBUG exclusion_word HIT!: ')
#                        print(ew)
#                        print(r['Item']['itemCaption'])
#                        continue

#                print('単位: ' + fl['notation_unit'])
                _a_title = a_title.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
                if fl['notation_unit'] == 'g':
                    # タイトルから重量取得
                    for i in sorted(re.findall(r'([0-9]+)g', _a_title), key=int):
                        # 一番小さい数字を使って割る
                        if int(i) > 1:
#                            print(str(i) + fl['notation_unit'])
                            a_amino_price=math.ceil(a_price/(int(i)/100))
                            break
                    # 取得できなかったらkgでサーチ
                    if a_amino_price == a_price:
                        for i in sorted(re.findall(r'([0-9]+\.[0-9]+|[0-9]+)kg', _a_title.replace(',', '.')), key=float):
                            if float(i) > 0:
#                                print(str(i) + fl['notation_unit'])
                                a_amino_price=math.ceil(a_price/((float(i)*1000)/100))
                                break

                elif fl['notation_unit'] == 'ml':
                    # mlの前にある数字を全部集める
                    for i in sorted(re.findall(r'([0-9]+)ml', _a_title), key=int):
                        if int(i) > 1:
                            a_amino_price=math.ceil(a_price/(int(i)/100))
                            break
                    # 業務用はL表示なので合わせる
                    if a_amino_price == a_price:
                        for i in sorted(re.findall(r'([0-9]+)L', _a_title), key=int):
                            if int(i) > 1:
                                a_amino_price=math.ceil(a_price/((float(i)*1000)/100))
                                break

                elif fl['notation_unit'] == '枚':
                    # 枚の前にある数字を全部集める
                    for i in sorted(re.findall(r'([0-9]+)枚', _a_title), key=int, reverse=True):
                        if int(i) > 1:
                            a_amino_price=math.ceil(a_price/int(i))
                            break
                    # デスクリプション
#                    if a_amino_price == a_price:
#                        for i in sorted(re.findall(r'([0-9]+)枚', a_description_text), key=int, reverse=True):
#                            if int(i) > 1:
#                                a_amino_price=math.ceil(a_price/int(i))
#                                break

                # 単価が取得できなければDBに入れない
                if a_amino_price == a_price:
                    continue

                a_site_url = 'https://www.amazon.co.jp/gp/product/' + div.get('data-asin') + '/ref=as_li_tl?ie=UTF8&tag=zagan06-22&camp=247&creative=1211&linkCode=as2&creativeASIN=' + div.get('data-asin')

                a_image_url = div.find('img', class_='s-image').get('src')

                # 送料チェック
                a_shipping_price=None
                if div.find('i', attrs={'aria-label': 'Amazon プライム'}):
                    a_shipping_price=0
                    print(div.find('i', attrs={'aria-label': 'Amazon プライム'}).get('aria-label'))
                if div.find('span', attrs={'dir': 'auto'}):
                    a_shipping_price=0
                    print(div.find('span', attrs={'dir': 'auto'}).get_text())

                print('amazon_site_url: ' + a_site_url)
                print('amazon_image_url: ' + a_image_url)
                print('amazon_title : ' + a_title)
                print('_amazon_title: ' + _a_title)
                print('amazon_price: ' + str(a_price))
                print('amazon_amino_price: ' + str(a_amino_price))
                print('amazon_shipping_price: ' + str(a_shipping_price))
                print('')

                Item.objects.update_or_create(site_url=a_site_url, defaults={'title': a_title[:200], 'image_url': a_image_url, 'site_url': a_site_url, 'amino_price': a_amino_price, 'price': a_price, 'distributor': 'amazon', 'shipping_price': a_shipping_price, })
                item = Item.objects.get(site_url=a_site_url)
                for tag in fl['tags']:
                    item.tags.add(tag)

