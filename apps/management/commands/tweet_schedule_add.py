from django.core.management import BaseCommand
from ...models import Item, TweetAccount, TweetSchedule

import datetime
import pytz
import tweepy


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

        TO_DATE = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        LAST_DATE = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))-datetime.timedelta(days=2)
        TWEET_DATE = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

        # ツイートアカウント情報げっちゅ
        ta=TweetAccount.objects.get(pk=1)

        # マスクツイート作成
        item_list_MASK = Item.objects.filter(updated_at__range=(LAST_DATE, TO_DATE), unit_price__range=('30', '1000000'), item_type=Item.ItemType.MASK, active=True).order_by('unit_price', '-updated_at').all()[:1]

        FREESHIPPING=''
        if item_list_MASK[0].freeshipping:
            FREESHIPPING='送料無料'

        import textwrap
        text='マスク在庫情報\nhttps://stock.the-menz.com\n{}\n{:,} 円/枚 {:,}円 {}\n{}\n#マスク #入荷 #再入荷 #在庫復活'.format(
                textwrap.fill(item_list_MASK[0].title, 62, max_lines=1, placeholder='…'),
                item_list_MASK[0].unit_price,
                item_list_MASK[0].price,
                FREESHIPPING,
                item_list_MASK[0].site_url
                )

        ts = TweetSchedule(tweet_account=ta, tweet_content=text, tweet_at=TWEET_DATE, tweeted=False)
        ts.save()

        # アルコールスプレーツイート作成
        item_list_ALCOHOL_SPRAY = Item.objects.filter(updated_at__range=(LAST_DATE, TO_DATE), unit_price__range=('0', '1000000'), item_type=Item.ItemType.ALCOHOL_SPRAY, active=True).order_by('unit_price', '-updated_at')

        FREESHIPPING=''
        if item_list_ALCOHOL_SPRAY[0].freeshipping:
            FREESHIPPING='送料無料'

        import textwrap
        text='アルコールスプレー在庫情報\nhttps://stock.the-menz.com/alcohol_spray/\n{}\n{:,} 円/1ml {:,}円 {}\n{}\n#アルコールスプレー #消毒 #除菌 #入荷 #再入荷 #在庫復活'.format(
                textwrap.fill(item_list_ALCOHOL_SPRAY[0].title, 62, max_lines=1, placeholder='…'),
                item_list_ALCOHOL_SPRAY[0].unit_price,
                item_list_ALCOHOL_SPRAY[0].price,
                FREESHIPPING,
                item_list_ALCOHOL_SPRAY[0].site_url
                )

        ts = TweetSchedule(tweet_account=ta, tweet_content=text, tweet_at=TWEET_DATE, tweeted=False)
        ts.save()

        # アルコールジェルツイート作成
        item_list_ALCOHOL_GEL = Item.objects.filter(updated_at__range=(LAST_DATE, TO_DATE), unit_price__range=('0', '1000000'), item_type=Item.ItemType.ALCOHOL_GEL, active=True).order_by('unit_price', '-updated_at')

        FREESHIPPING=''
        if item_list_ALCOHOL_GEL[0].freeshipping:
            FREESHIPPING='送料無料'

        import textwrap
        text='アルコールジェル在庫情報\nhttps://stock.the-menz.com/alcohol_gel/\n{}\n{:,} 円/1ml {:,}円 {}\n{}\n#アルコールジェル #消毒 #除菌 #入荷 #再入荷 #在庫復活'.format(
                textwrap.fill(item_list_ALCOHOL_GEL[0].title, 62, max_lines=1, placeholder='…'),
                item_list_ALCOHOL_GEL[0].unit_price,
                item_list_ALCOHOL_GEL[0].price,
                FREESHIPPING,
                item_list_ALCOHOL_GEL[0].site_url
                )

        ts = TweetSchedule(tweet_account=ta, tweet_content=text, tweet_at=TWEET_DATE, tweeted=False)
        ts.save()

