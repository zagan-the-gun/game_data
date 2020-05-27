from django.core.management import BaseCommand
from ...models import Item, TweetAccount, TweetSchedule

import datetime
import pytz
import tweepy

import textwrap


class Command(BaseCommand):
    help = 'ツイートスケジュール追加'

#    def add_arguments(self, parser):
#        parser.add_argument('-c', '--command', dest='command', help='add or del')
#        parser.add_argument('opt1', help='必須オプション')
#        parser.add_argument('--opt2', help='任意オプション')
#        parser.add_argument('--date', help='何日前')
 
    def handle(self, *args, **options):
#        print(options['command'])
        self.stdout.write(self.style.SUCCESS('DEBUG DEBUG DEBUG tweet_schedule_add: '))
#        self.stdout.write(options.__str__())

#        TO_DATE = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
#        LAST_DATE = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))-datetime.timedelta(days=5)
#        TWEET_DATE = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

        TO_DATE = pytz.timezone('Asia/Tokyo').localize(datetime.datetime.now())
        LAST_DATE = pytz.timezone('Asia/Tokyo').localize(datetime.datetime.now()-datetime.timedelta(days=5))
        TWEET_DATE = pytz.timezone('Asia/Tokyo').localize(datetime.datetime.now())
        print(TO_DATE)
        print(LAST_DATE)
        print(TWEET_DATE)

        # ツイートアカウント情報げっちゅ
        ta=TweetAccount.objects.get(pk=1)

        # カニツイート作成
        item_list_KANI = Item.objects.filter(updated_at__range=(LAST_DATE, TO_DATE), amino_price__range=('0', '1000000'), item_type=Item.ItemType.KAISEN_KANI, active=True).order_by('amino_price', '-updated_at').all()[:1]

        SHIPPING=''
        if item_list_KANI[0].shipping_price == 0:
            SHIPPING = '送料無料'
        elif item_list_KANI[0].shipping_price is None:
            SHIPPING = ''
        else:
            SHIPPING = '+送料({}円)'.format(item_list_KANI[0].shipping_price)

        text='海鮮在庫速報\nhttps://kaisen.stock-news.work\n{}\n{:,} 円/100g {:,}円 {}\n{}\n#海鮮 #カニ #蟹 #BBQ'.format(
                textwrap.fill(item_list_KANI[0].title, 62, max_lines=1, placeholder='…'),
                item_list_KANI[0].amino_price,
                item_list_KANI[0].price,
                SHIPPING,
                item_list_KANI[0].site_url
                )

        ts = TweetSchedule(tweet_account=ta, tweet_content=text, tweet_at=TWEET_DATE, tweeted=False)
        ts.save()


        # エビツイート作成
        item_list_EBI = Item.objects.filter(updated_at__range=(LAST_DATE, TO_DATE), amino_price__range=('0', '1000000'), item_type=Item.ItemType.KAISEN_EBI, active=True).order_by('amino_price', '-updated_at').all()[:1]

        SHIPPING=''
        if item_list_EBI[0].shipping_price == 0:
            SHIPPING = '送料無料'
        elif item_list_EBI[0].shipping_price is None:
            SHIPPING = ''
        else:
            SHIPPING = '+送料({}円)'.format(item_list_EBI[0].shipping_price)

        text='海鮮在庫速報\nhttps://kaisen.stock-news.work\n{}\n{:,} 円/100g {:,}円 {}\n{}\n#海鮮 #エビ #海老 #BBQ'.format(
                textwrap.fill(item_list_EBI[0].title, 62, max_lines=1, placeholder='…'),
                item_list_EBI[0].amino_price,
                item_list_EBI[0].price,
                SHIPPING,
                item_list_EBI[0].site_url
                )

        ts = TweetSchedule(tweet_account=ta, tweet_content=text, tweet_at=TWEET_DATE, tweeted=False)
        ts.save()


        # カキツイート作成
        item_list_KAKI = Item.objects.filter(updated_at__range=(LAST_DATE, TO_DATE), amino_price__range=('0', '1000000'), item_type=Item.ItemType.KAISEN_KAKI, active=True).order_by('amino_price', '-updated_at').all()[:1]

        SHIPPING=''
        if item_list_KAKI[0].shipping_price == 0:
            SHIPPING = '送料無料'
        elif item_list_KAKI[0].shipping_price is None:
            SHIPPING = ''
        else:
            SHIPPING = '+送料({}円)'.format(item_list_KAKI[0].shipping_price)

        text='海鮮在庫速報\nhttps://kaisen.stock-news.work\n{}\n{:,} 円/100g {:,}円 {}\n{}\n#海鮮 #カキ #牡蠣 #BBQ'.format(
                textwrap.fill(item_list_KAKI[0].title, 62, max_lines=1, placeholder='…'),
                item_list_KAKI[0].amino_price,
                item_list_KAKI[0].price,
                SHIPPING,
                item_list_KAKI[0].site_url
                )

        ts = TweetSchedule(tweet_account=ta, tweet_content=text, tweet_at=TWEET_DATE, tweeted=False)
        ts.save()

