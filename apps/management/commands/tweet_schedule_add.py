from django.core.management import BaseCommand
from ...models import Item, SmallCategory, TweetAccount, TweetSchedule

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

        #pytz.timezone('Asia/Tokyo').localize(datetime.datetime.now())
        TODATE = pytz.timezone('Asia/Tokyo').localize(datetime.datetime.now())
        LAST_DATE = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))-datetime.timedelta(days=2)
        TWEET_DATE = datetime.datetime.now(pytz.timezone('Asia/Tokyo')) + datetime.timedelta(hours=1)

        # ツイートアカウント情報げっちゅ
        ta=TweetAccount.objects.get(pk=1)

        # スモールカテゴリ基準でグルグル回す
        for s in SmallCategory.objects.filter(is_view = True):
            tag_list = u", ".join(t.name for t in s.tags.all())
            item = Item.objects.filter(updated_at__range=(LAST_DATE, TODATE), amino_price__range=('0', '1000000'), tags__name__in=[tag_list], active=True).order_by('amino_price', '-updated_at').all()[:1]
            FREESHIPPING=''
            if item[0].shipping_price == 0:
                FREESHIPPING='送料無料'

            URL = 'https://zaikokun.work/stock-news/' + s.medium_category.large_category.name + '/' + s.medium_category.name + '/' + s.name + '/'
            text = '{}在庫情報【安値更新】\n{:,} 円/{} {} {:,}円\n{}\n{}\n{}'.format(
                     s.label,
                     item[0].amino_price,
                     s.notation_per_unit,
                     FREESHIPPING,
                     item[0].price,
                     URL,
                     textwrap.fill(item[0].title, 62, max_lines=1, placeholder='…'),
                     s.hashtag,
                   )
#            print(type(TWEET_DATE))
#            print(TODATE)
#            print(LAST_DATE)
#            print(TWEET_DATE)
#            print(text)
#            print('')
#            print('')

            TweetSchedule.objects.get_or_create(tweet_account=ta, tweet_content=text, defaults={'tweet_account': ta, 'tweet_content': text, 'tweet_at': TWEET_DATE, 'tweeted': False, })
            #ts = TweetSchedule(tweet_account=ta, tweet_content=text, tweet_at=TWEET_DATE, tweeted=False)
            #ts.save()
            TWEET_DATE = TWEET_DATE + datetime.timedelta(minutes=1)

